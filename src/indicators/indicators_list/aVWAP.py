import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators

def calculate_avwap_channel(df,
                           peaks_valleys=False,
                           peaks_valleys_avg=False,
                           peaks_avg=False,
                           valleys_avg=False,
                           gaps=False, 
                           gaps_avg=False,
                           OB=False,
                           OB_avg=False,
                           BoS_CHoCH=False,
                           BoS_CHoCH_avg=False,
                           All_avg=False,
                           peaks_valleys_params=None,
                           gaps_params=None,
                           OB_params=None,
                           BoS_CHoCH_params=None,
                           avg_lookback=25,
                           keep_OB_column=False,
                           aVWAP_channel=False):
    """
    Calculate anchored VWAP channels from market structure points.

    New Parameters:
        BoS_CHoCH: Calculate aVWAPs from BoS/CHoCH ranges
        BoS_CHoCH_avg: Calculate rolling average of BoS/CHoCH aVWAPs
        BoS_CHoCH_params: {
            'swing_length': 25,
            'max_aVWAPs': None
        }
    """
    # Set default parameters if not provided
    if peaks_valleys_params is None:
        peaks_valleys_params = {'periods': 25, 'max_aVWAPs': None}
    if gaps_params is None:
        gaps_params = {'max_aVWAPs': None}
    if OB_params is None:
        OB_params = {
            'periods': 25, 
            'max_aVWAPs': None,
            'include_bullish': True,
            'include_bearish': True
        }
    if BoS_CHoCH_params is None:
        BoS_CHoCH_params = {
            'swing_length': 25,
            'max_aVWAPs': None
        }

    # Get indicators based on input parameters
    aVWAP_anchors = []
    if peaks_valleys or peaks_valleys_avg or peaks_avg or valleys_avg or All_avg: 
        aVWAP_anchors.append('peaks_valleys')
    if gaps or gaps_avg or All_avg: 
        aVWAP_anchors.append('gaps')
    if OB or OB_avg or All_avg: 
        aVWAP_anchors.append('OB')
    if BoS_CHoCH or BoS_CHoCH_avg or All_avg:
        aVWAP_anchors.append('BoS_CHoCH')

    if not aVWAP_anchors:
        return {}

    params = {}
    if peaks_valleys or peaks_valleys_avg or peaks_avg or valleys_avg or All_avg: 
        params['peaks_valleys'] = {'periods': peaks_valleys_params['periods']}
    if gaps or gaps_avg or All_avg: 
        params['gaps'] = {}
    if OB or OB_avg or All_avg: 
        params['OB'] = {'periods': OB_params['periods']}
    if BoS_CHoCH or BoS_CHoCH_avg or All_avg:
        params['BoS_CHoCH'] = {'swing_length': BoS_CHoCH_params['swing_length']}

    # print('\n')
    # print(aVWAP_anchors)
    # print(params)
    # print('\n')

    df = get_indicators(df, aVWAP_anchors, params)
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])

    # Initialize storage dictionaries
    peaks_valleys_aVWAPs = {}
    peaks_only_aVWAPs = {}
    valleys_only_aVWAPs = {}
    gaps_aVWAPs = {}
    OB_aVWAPs = {}
    BoS_CHoCH_aVWAPs = {}

    # Track extreme points for channel calculation
    highest_peak_idx = None
    lowest_valley_idx = None

    def process_anchors(indices, prefix, storage_dict, max_count=None):
        if not indices:
            return
        sorted_indices = sorted(indices, reverse=True)
        if max_count is not None:
            sorted_indices = sorted_indices[:max_count]
        for i in sorted_indices:
            storage_dict[f'{prefix}_{i}'] = calculate_avwap(df, i)

    # Process peaks and valleys
    if peaks_valleys or peaks_valleys_avg or peaks_avg or valleys_avg or All_avg:
        peaks_indices = df[df['Peaks'] == 1].index.tolist() if 'Peaks' in df.columns else []
        valleys_indices = df[df['Valleys'] == 1].index.tolist() if 'Valleys' in df.columns else []
        
        if aVWAP_channel:
            if peaks_indices:
                peak_prices = df.loc[peaks_indices, 'High']
                highest_peak_idx = peaks_indices[peak_prices.argmax()]
                peaks_indices = [i for i in peaks_indices if i >= highest_peak_idx]
            
            if valleys_indices:
                valley_prices = df.loc[valleys_indices, 'Low']
                lowest_valley_idx = valleys_indices[valley_prices.argmin()]
                valleys_indices = [i for i in valleys_indices if i >= lowest_valley_idx]
        
        process_anchors(peaks_indices, 'aVWAP_peak', peaks_only_aVWAPs, 
                       peaks_valleys_params.get('max_aVWAPs'))
        process_anchors(valleys_indices, 'aVWAP_valley', valleys_only_aVWAPs, 
                       peaks_valleys_params.get('max_aVWAPs'))
        
        peaks_valleys_aVWAPs = {**peaks_only_aVWAPs, **valleys_only_aVWAPs}

        if peaks_valleys_avg and peaks_valleys_aVWAPs:
            if aVWAP_channel:
                if highest_peak_idx is not None and lowest_valley_idx is not None:
                    first_valid_idx = max(highest_peak_idx, lowest_valley_idx)
                    temp_avg = calculate_rolling_aVWAP_avg(df, peaks_valleys_aVWAPs, avg_lookback)
                    df['Peaks_Valleys_avg'] = temp_avg.where(df.index >= first_valid_idx)
                else:
                    df['Peaks_Valleys_avg'] = np.nan
            else:
                df['Peaks_Valleys_avg'] = calculate_rolling_aVWAP_avg(df, peaks_valleys_aVWAPs, avg_lookback)

    # Process gaps
    if gaps or gaps_avg or All_avg:
        gap_up_indices = df[df['Gap_Up'] == 1].index.tolist() if 'Gap_Up' in df.columns else []
        gap_down_indices = df[df['Gap_Down'] == 1].index.tolist() if 'Gap_Down' in df.columns else []
        
        process_anchors(gap_up_indices, 'Gap_Up_aVWAP', gaps_aVWAPs, 
                       gaps_params.get('max_aVWAPs'))
        process_anchors(gap_down_indices, 'Gap_Down_aVWAP', gaps_aVWAPs, 
                       gaps_params.get('max_aVWAPs'))

    # Process OBs
    if OB or OB_avg or All_avg:
        OB_bull_indices = []
        OB_bear_indices = []
        
        if 'OB' in df.columns:
            if aVWAP_channel:
                if lowest_valley_idx is not None:
                    OB_bull_indices = df[(df['OB'] == 1) & (df.index >= lowest_valley_idx)].index.tolist()
                if highest_peak_idx is not None:
                    OB_bear_indices = df[(df['OB'] == -1) & (df.index >= highest_peak_idx)].index.tolist()
            else:
                OB_bull_indices = df[df['OB'] == 1].index.tolist() if OB_params.get('include_bullish', True) else []
                OB_bear_indices = df[df['OB'] == -1].index.tolist() if OB_params.get('include_bearish', True) else []
        
        process_anchors(OB_bull_indices, 'aVWAP_OB_bull', OB_aVWAPs, 
                       OB_params.get('max_aVWAPs'))
        process_anchors(OB_bear_indices, 'aVWAP_OB_bear', OB_aVWAPs, 
                       OB_params.get('max_aVWAPs'))

    # Process BoS/CHoCH ranges
    if BoS_CHoCH or BoS_CHoCH_avg or All_avg:
        def process_BoS_CHoCH_range(signal_idx, break_idx, signal_type):
            """Calculate VWAP from extreme point in signal→break range"""
            if pd.isna(break_idx) or break_idx <= signal_idx:
                return None
                
            range_df = df.iloc[signal_idx:break_idx+1]
            
            if signal_type == 'bullish':
                # Find lowest low in range for bullish signals
                extreme_idx = range_df['Low'].idxmin()
            else:  # bearish
                # Find highest high in range for bearish signals
                extreme_idx = range_df['High'].idxmax()
            
            return calculate_avwap(df, extreme_idx)

        # Process bullish signals (BoS=1 or CHoCH=1)
        bullish_signals = df[(df['BoS'] == 1) | (df['CHoCH'] == 1)].index
        for idx in bullish_signals:
            break_idx = int(df.loc[idx, 'BoS_CHoCH_Break_Index']) if not pd.isna(df.loc[idx, 'BoS_CHoCH_Break_Index']) else None
            if break_idx:
                vwap = process_BoS_CHoCH_range(idx, break_idx, 'bullish')
                if vwap is not None:
                    BoS_CHoCH_aVWAPs[f'aVWAP_BoS_CHoCH_bull_{idx}'] = vwap
        
        # Process bearish signals (BoS=-1 or CHoCH=-1)
        bearish_signals = df[(df['BoS'] == -1) | (df['CHoCH'] == -1)].index
        for idx in bearish_signals:
            break_idx = int(df.loc[idx, 'BoS_CHoCH_Break_Index']) if not pd.isna(df.loc[idx, 'BoS_CHoCH_Break_Index']) else None
            if break_idx:
                vwap = process_BoS_CHoCH_range(idx, break_idx, 'bearish')
                if vwap is not None:
                    BoS_CHoCH_aVWAPs[f'aVWAP_BoS_CHoCH_bear_{idx}'] = vwap

    all_aVWAPs = {**peaks_valleys_aVWAPs, **gaps_aVWAPs, **OB_aVWAPs, **BoS_CHoCH_aVWAPs}

    if not all_aVWAPs: 
        return {}

    df = pd.concat([df, pd.DataFrame(all_aVWAPs)], axis=1)

    # Calculate averages
    if peaks_avg and peaks_only_aVWAPs:
        df['Peaks_avg'] = calculate_rolling_aVWAP_avg(df, peaks_only_aVWAPs, avg_lookback)
    
    if valleys_avg and valleys_only_aVWAPs:
        df['Valleys_avg'] = calculate_rolling_aVWAP_avg(df, valleys_only_aVWAPs, avg_lookback)

    if gaps_avg and gaps_aVWAPs:                   
        df['Gaps_avg'] = calculate_rolling_aVWAP_avg(df, gaps_aVWAPs, avg_lookback)

    if OB_avg and OB_aVWAPs:                       
        df['OB_avg'] = calculate_rolling_aVWAP_avg(df, OB_aVWAPs, avg_lookback)

    if BoS_CHoCH_avg and BoS_CHoCH_aVWAPs:
        df['BoS_CHoCH_avg'] = calculate_rolling_aVWAP_avg(df, BoS_CHoCH_aVWAPs, avg_lookback)

    if All_avg and all_aVWAPs:
        df['All_avg'] = calculate_rolling_aVWAP_avg(df, all_aVWAPs, avg_lookback)

    # Format output
    cols_to_drop = ['Open', 'Close', 'High', 'Low', 'Volume']
    if peaks_valleys or peaks_valleys_avg or peaks_avg or valleys_avg or All_avg:
        cols_to_drop.extend(['Valleys', 'Peaks'])
    if gaps or gaps_avg or All_avg:
        cols_to_drop.extend(['Gap_Up', 'Gap_Down'])
    if not keep_OB_column:
        cols_to_drop.extend(['OB', 'OB_High', 'OB_Low', 'OB_Mitigated_Index'])
    if BoS_CHoCH or BoS_CHoCH_avg:
        cols_to_drop.extend(['BoS', 'CHoCH', 'BoS_CHoCH_Price', 'BoS_CHoCH_Break_Index'])

    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    df.set_index('date', inplace=True)

    # Prepare results
    result_dict = {}
    if peaks_valleys and peaks_valleys_aVWAPs:
        result_dict.update({col: df[col] for col in peaks_valleys_aVWAPs})
    if gaps and gaps_aVWAPs:
        result_dict.update({col: df[col] for col in gaps_aVWAPs})
    if OB and OB_aVWAPs:
        if OB_params.get('include_bullish', True):
            bull_cols = [col for col in OB_aVWAPs if col.startswith('aVWAP_OB_bull')]
            result_dict.update({col: df[col] for col in bull_cols})
        if OB_params.get('include_bearish', True):
            bear_cols = [col for col in OB_aVWAPs if col.startswith('aVWAP_OB_bear')]
            result_dict.update({col: df[col] for col in bear_cols})
    if BoS_CHoCH and BoS_CHoCH_aVWAPs:
        bull_cols = [col for col in BoS_CHoCH_aVWAPs if col.startswith('aVWAP_BoS_CHoCH_bull')]
        result_dict.update({col: df[col] for col in bull_cols})
        bear_cols = [col for col in BoS_CHoCH_aVWAPs if col.startswith('aVWAP_BoS_CHoCH_bear')]
        result_dict.update({col: df[col] for col in bear_cols})
        
    if keep_OB_column:
        result_dict.update({
            'OB': df['OB'],
            'OB_High': df['OB_High'],
            'OB_Low': df['OB_Low'],
            'OB_Mitigated_Index': df['OB_Mitigated_Index']
        })

    # Add averages
    avg_columns = [
        ('Peaks_Valleys_avg', peaks_valleys_avg),
        ('Peaks_avg', peaks_avg),
        ('Valleys_avg', valleys_avg),
        ('Gaps_avg', gaps_avg),
        ('OB_avg', OB_avg),
        ('BoS_CHoCH_avg', BoS_CHoCH_avg),
        ('All_avg', All_avg)
    ]
    
    for col, flag in avg_columns:
        if flag and col in df.columns:
            result_dict[col] = df[col]

    return result_dict

def calculate_indicator(df, **params):
    return calculate_avwap_channel(df, **params)

def calculate_avwap(df, anchor_index):
    """Calculate anchored VWAP from anchor point"""
    df_anchored = df.iloc[anchor_index:].copy()
    df_anchored['cumulative_volume'] = df_anchored['Volume'].cumsum()
    df_anchored['cumulative_volume_price'] = (df_anchored['Volume'] * 
        (df_anchored['High'] + df_anchored['Low'] + df_anchored['Close']) / 3).cumsum()
    return df_anchored['cumulative_volume_price'] / df_anchored['cumulative_volume']

def calculate_rolling_aVWAP_avg(df, aVWAP_dict, lookback=None):
    """Calculate average of aVWAP values"""
    aVWAP_df = pd.DataFrame(aVWAP_dict)
    sorted_cols = sorted(aVWAP_df.columns, key=lambda x: int(x.split('_')[-1]), reverse=True)
    aVWAP_df = aVWAP_df[sorted_cols]
    
    avg_values = pd.Series(np.nan, index=df.index)
    for idx in aVWAP_df.index.intersection(df.index):
        valid_vals = aVWAP_df.loc[idx].dropna()
        if lookback is not None:
            valid_vals = valid_vals[:lookback]
        if len(valid_vals) > 0:
            avg_values.loc[idx] = valid_vals.mean()
    return avg_values
