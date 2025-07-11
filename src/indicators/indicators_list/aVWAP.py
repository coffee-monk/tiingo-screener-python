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
                           All_avg=False,
                           peaks_valleys_params=None,
                           gaps_params=None,
                           OB_params=None,
                           avg_lookback=1,
                           keep_OB_column=False,
                           aVWAP_channel=False):
    """
    Calculate anchored VWAP channels with separate parameters for each type.
    
    Example:
        calculate_avwap_channel(
            df,
            peaks_valleys=True,
            peaks_avg=True,
            valleys_avg=True,
            aVWAP_channel=True,
            peaks_valleys_params={'periods': 30, 'max_aVWAPs': 10},
            OB=True,
            OB_params={'periods': 20, 'max_aVWAPs': 5},
            avg_lookback=3,
            keep_OB_column=False
        )
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with price data
    peaks_valleys : bool
        Whether to calculate peaks/valleys aVWAPs
    peaks_valleys_avg : bool
        Whether to calculate peaks/valleys aVWAP average
    peaks_avg : bool
        Whether to calculate peaks-only aVWAP average
    valleys_avg : bool
        Whether to calculate valleys-only aVWAP average
    gaps : bool
        Whether to calculate gap aVWAPs
    gaps_avg : bool
        Whether to calculate gap aVWAP average
    OB : bool
        Whether to calculate OB aVWAPs
    OB_avg : bool
        Whether to calculate OB aVWAP average
    All_avg : bool
        Whether to calculate average of all aVWAPs
    peaks_valleys_params : dict
        Parameters for peaks/valleys calculation:
        - periods: int (for peak/valley detection)
        - max_aVWAPs: int or None (max number to calculate)
    gaps_params : dict
        Parameters for gaps calculation:
        - max_aVWAPs: int or None (max number to calculate)
    OB_params : dict
        Parameters for OB calculation:
        - periods: int (for OB detection)
        - max_aVWAPs: int or None (max number to calculate)
    avg_lookback : int
        Number of most recent aVWAPs to include in average calculation
    keep_OB_column : bool
        Whether to keep the 'OB' column in the final output
    aVWAP_channel : bool
        If True, only uses:
        - Valleys starting from the LOWEST price
        - Peaks starting from the HIGHEST price
    """
    
    # Set default parameters if not provided
    if peaks_valleys_params is None:
        peaks_valleys_params = {'periods': 25, 'max_aVWAPs': None}
    if gaps_params is None:
        gaps_params = {'max_aVWAPs': None}
    if OB_params is None:
        OB_params = {'periods': 25, 'max_aVWAPs': None}

    # Get indicators based on input parameters
    aVWAP_anchors = []
    if peaks_valleys or peaks_valleys_avg or peaks_avg or valleys_avg or All_avg: 
        aVWAP_anchors.append('peaks_valleys')
    if gaps or gaps_avg or All_avg: 
        aVWAP_anchors.append('gaps')
    if OB or OB_avg or All_avg: 
        aVWAP_anchors.append('OB')

    if not aVWAP_anchors:  # If no anchor types selected
        return {}

    params = {}
    if peaks_valleys or peaks_valleys_avg or peaks_avg or valleys_avg or All_avg: 
        params['peaks_valleys'] = {'periods': peaks_valleys_params['periods']}
    if gaps or gaps_avg or All_avg: 
        params['gaps'] = {}
    if OB or OB_avg or All_avg: 
        params['OB'] = {'periods': OB_params['periods']}

    df = get_indicators(df, aVWAP_anchors, params)
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])

    # Initialize separate dictionaries for each aVWAP type
    peaks_valleys_aVWAPs = {}
    peaks_only_aVWAPs = {}
    valleys_only_aVWAPs = {}
    gaps_aVWAPs = {}
    OB_aVWAPs = {}

    # Modified anchor point processing with limit
    def process_anchors(indices, prefix, storage_dict, max_count=None):
        if not indices:
            return
        
        # Sort indices descending (newest first)
        sorted_indices = sorted(indices, reverse=True)
        
        # Apply limit if specified
        if max_count is not None:
            sorted_indices = sorted_indices[:max_count]
        
        for i in sorted_indices:
            storage_dict[f'{prefix}_{i}'] = calculate_avwap(df, i)

    # Calculate peaks/valleys aVWAPs
    if peaks_valleys or peaks_valleys_avg or peaks_avg or valleys_avg or All_avg:
        peaks_indices = df[df['Peaks'] == 1].index.tolist() if 'Peaks' in df.columns else []
        valleys_indices = df[df['Valleys'] == 1].index.tolist() if 'Valleys' in df.columns else []
        
        # NEW: Filter for most extreme points if aVWAP_channel is True
        if aVWAP_channel:
            if peaks_indices:
                peak_prices = df.loc[peaks_indices, 'High']
                highest_peak_idx = peaks_indices[peak_prices.argmax()]
                peaks_indices = [i for i in peaks_indices if i >= highest_peak_idx]
            
            if valleys_indices:
                valley_prices = df.loc[valleys_indices, 'Low']
                lowest_valley_idx = valleys_indices[valley_prices.argmin()]
                valleys_indices = [i for i in valleys_indices if i >= lowest_valley_idx]
        
        # Process peaks and valleys separately
        process_anchors(peaks_indices, 'aVWAP_peak', peaks_only_aVWAPs, 
                       peaks_valleys_params.get('max_aVWAPs'))
        process_anchors(valleys_indices, 'aVWAP_valley', valleys_only_aVWAPs, 
                       peaks_valleys_params.get('max_aVWAPs'))
        
        # Combine for the general peaks_valleys storage
        peaks_valleys_aVWAPs = {**peaks_only_aVWAPs, **valleys_only_aVWAPs}

    # Calculate gap aVWAPs
    if gaps or gaps_avg or All_avg:
        gap_up_indices = df[df['Gap_Up'] == 1].index.tolist() if 'Gap_Up' in df.columns else []
        gap_down_indices = df[df['Gap_Down'] == 1].index.tolist() if 'Gap_Down' in df.columns else []
        
        process_anchors(gap_up_indices, 'Gap_Up_aVWAP', gaps_aVWAPs, 
                       gaps_params.get('max_aVWAPs'))
        process_anchors(gap_down_indices, 'Gap_Down_aVWAP', gaps_aVWAPs, 
                       gaps_params.get('max_aVWAPs'))

    # Calculate OB aVWAPs
    if OB or OB_avg or All_avg:
        OB_bull_indices = df[df['OB'] == 1].index.tolist() if 'OB' in df.columns else []
        OB_bear_indices = df[df['OB'] == -1].index.tolist() if 'OB' in df.columns else []
        
        process_anchors(OB_bull_indices, 'aVWAP_OB_bull', OB_aVWAPs, 
                       OB_params.get('max_aVWAPs'))
        process_anchors(OB_bear_indices, 'aVWAP_OB_bear', OB_aVWAPs, 
                       OB_params.get('max_aVWAPs'))

    all_aVWAPs = {**peaks_valleys_aVWAPs, **gaps_aVWAPs, **OB_aVWAPs}

    # If no anchor points found
    if not all_aVWAPs: 
        return {}

    # Add all aVWAP columns to dataframe
    df = pd.concat([df, pd.DataFrame(all_aVWAPs)], axis=1) 

    # Calculate averages if requested
    if peaks_valleys_avg and peaks_valleys_aVWAPs: 
        df['Peaks_Valleys_avg'] = calculate_rolling_aVWAP_avg(df, peaks_valleys_aVWAPs, avg_lookback)
    
    if peaks_avg and peaks_only_aVWAPs:
        df['Peaks_avg'] = calculate_rolling_aVWAP_avg(df, peaks_only_aVWAPs, avg_lookback)
    
    if valleys_avg and valleys_only_aVWAPs:
        df['Valleys_avg'] = calculate_rolling_aVWAP_avg(df, valleys_only_aVWAPs, avg_lookback)

    if gaps_avg and gaps_aVWAPs:                   
        df['Gaps_avg'] = calculate_rolling_aVWAP_avg(df, gaps_aVWAPs, avg_lookback)

    if OB_avg and OB_aVWAPs:                       
        df['OB_avg'] = calculate_rolling_aVWAP_avg(df, OB_aVWAPs, avg_lookback)

    # Calculate average from all aVWAPs
    if All_avg and all_aVWAPs:
        df['All_avg'] = calculate_rolling_aVWAP_avg(df, all_aVWAPs, avg_lookback)

    # Format dataframe
    cols_to_drop = ['Open', 'Close', 'High', 'Low', 'Volume']
    if peaks_valleys or peaks_valleys_avg or peaks_avg or valleys_avg or All_avg:
        cols_to_drop.extend(['Valleys', 'Peaks'])
    if gaps or gaps_avg or All_avg:
        cols_to_drop.extend(['Gap_Up', 'Gap_Down'])
    if not keep_OB_column:
        cols_to_drop.extend(['OB', 'OB_High', 'OB_Low', 'OB_Mitigated_Index'])

    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    df.set_index('date', inplace=True)

    # Create final results dictionary
    result_dict = {}

    if peaks_valleys and peaks_valleys_aVWAPs:
        for col in peaks_valleys_aVWAPs:
            result_dict[col] = df[col]

    if gaps and gaps_aVWAPs:
        for col in gaps_aVWAPs:
            result_dict[col] = df[col]

    if OB and OB_aVWAPs:
        for col in OB_aVWAPs:
            result_dict[col] = df[col]
        if keep_OB_column:
            result_dict['OB'] = df['OB']
            result_dict['OB_High'] = df['OB_High']
            result_dict['OB_Low'] = df['OB_Low']
            result_dict['OB_Mitigated_Index'] = df['OB_Mitigated_Index']

    # Add averages if calculated
    if peaks_valleys_avg and 'Peaks_Valleys_avg' in df.columns:
        result_dict['Peaks_Valleys_avg'] = df['Peaks_Valleys_avg']
    if peaks_avg and 'Peaks_avg' in df.columns:
        result_dict['Peaks_avg'] = df['Peaks_avg']
    if valleys_avg and 'Valleys_avg' in df.columns:
        result_dict['Valleys_avg'] = df['Valleys_avg']
    if gaps_avg and 'Gaps_avg' in df.columns:
        result_dict['Gaps_avg'] = df['Gaps_avg']
    if OB_avg and 'OB_avg' in df.columns:
        result_dict['OB_avg'] = df['OB_avg']
    if All_avg and 'All_avg' in df.columns:
        result_dict['All_avg'] = df['All_avg']

    return result_dict

def calculate_indicator(df, **params):
    return calculate_avwap_channel(df, **params)

# Utils
def calculate_avwap(df, anchor_index):
    """Calculate anchored VWAP from anchor point"""
    df_anchored = df.iloc[anchor_index:].copy()
    df_anchored['cumulative_volume'] = df_anchored['Volume'].cumsum()
    df_anchored['cumulative_volume_price'] = (df_anchored['Volume'] * 
        (df_anchored['High'] + df_anchored['Low'] + df_anchored['Close']) / 3).cumsum()
    return df_anchored['cumulative_volume_price'] / df_anchored['cumulative_volume']

def calculate_rolling_aVWAP_avg(df, aVWAP_dict, lookback=None):
    """
    Calculate average of aVWAP values.
    - When lookback=None: Uses ALL available aVWAPs (default)
    - When lookback=N: Uses only the most recent N aVWAPs
    """
    aVWAP_df = pd.DataFrame(aVWAP_dict)
    
    # Sort columns by anchor recency (newest first)
    sorted_cols = sorted(aVWAP_df.columns, 
                        key=lambda x: int(x.split('_')[-1]), 
                        reverse=True)
    aVWAP_df = aVWAP_df[sorted_cols]
    
    avg_values = pd.Series(np.nan, index=df.index)
    
    for idx in aVWAP_df.index.intersection(df.index):
        valid_vals = aVWAP_df.loc[idx].dropna()
        
        # Apply lookback if specified
        if lookback is not None:
            valid_vals = valid_vals[:lookback]
        
        if len(valid_vals) > 0:
            avg_values.loc[idx] = valid_vals.mean()
    
    return avg_values
