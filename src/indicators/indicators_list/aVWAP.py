import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators

def calculate_avwap_channel(df, 
                            peaks_valleys=False, 
                            peaks_valleys_avg=False, 
                            gaps=False, 
                            gaps_avg=False, 
                            OB=True, 
                            OB_avg=False, 
                            periods=25,
                            avg_lookback=3, 
                            ):

    # Get indicators based on input parameters --------------------------------

    aVWAP_anchors = []
    if peaks_valleys or peaks_valleys_avg: aVWAP_anchors.append('peaks_valleys')
    if gaps or gaps_avg: aVWAP_anchors.append('gaps')
    if OB: aVWAP_anchors.append('OB')
 
    if not aVWAP_anchors:  # If no anchor types selected
        return {}

    params = {}
    if peaks_valleys: params['peaks_valleys'] = {'periods': periods}
    if gaps: params['gaps'] = {}
    if OB: params['OB'] = {'periods': periods}

    df = get_indicators(df, aVWAP_anchors, params)
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])

    # Initialize separate dictionaries for peaks/valleys and gaps -------------

    peaks_valleys_aVWAPs = {}
    gaps_aVWAPs = {}
    OB_aVWAPs = {}

    anchor_dates = {}

    # Calculate peaks/valleys/gaps-up/gaps-down aVWAPs ------------------------

    if peaks_valleys or peaks_valleys_avg:
        peaks_indices = df[df['Peaks'] == 1].index.tolist() if 'Peaks' in df.columns else []
        valleys_indices = df[df['Valleys'] == 1].index.tolist() if 'Valleys' in df.columns else []

        for i in peaks_indices:
            peaks_valleys_aVWAPs[f'aVWAP_peak_{i}'] = calculate_avwap(df, i)
            anchor_dates[f'aVWAP_peak_{i}'] = df.index[i]
        for i in valleys_indices:
            peaks_valleys_aVWAPs[f'aVWAP_valley_{i}'] = calculate_avwap(df, i)

    if gaps or gaps_avg:
        gap_up_indices = df[df['Gap_Up'] == 1].index.tolist() if 'Gap_Up' in df.columns else []
        gap_down_indices = df[df['Gap_Down'] == 1].index.tolist() if 'Gap_Down' in df.columns else []

        for i in gap_up_indices:
            gaps_aVWAPs[f'Gap_aVWAP_{i}'] = calculate_avwap(df, i)
        for i in gap_down_indices:
            gaps_aVWAPs[f'Gap_aVWAP_{i}'] = calculate_avwap(df, i)

    if OB:
        OB_bull_indices = df[df['OB'] == 1].index.tolist()  if 'OB' in df.columns else []
        OB_bear_indices = df[df['OB'] == -1].index.tolist() if 'OB' in df.columns else []

        for i in OB_bull_indices:
            OB_aVWAPs[f'aVWAP_OB_bull_{i}'] = calculate_avwap(df, i)
        for i in OB_bear_indices:
            OB_aVWAPs[f'aVWAP_OB_bear_{i}'] = calculate_avwap(df, i)

    all_aVWAPs = {**peaks_valleys_aVWAPs, **gaps_aVWAPs, **OB_aVWAPs} # Combine all aVWAPs

    # If no anchor points found
    if not all_aVWAPs: return {}

    # Add all aVWAP columns to dataframe
    df = pd.concat([df, pd.DataFrame(all_aVWAPs)], axis=1) 

    # Calculate averages if requested -----------------------------------------

    if peaks_valleys_avg and peaks_valleys_aVWAPs:
        df['Peaks_Valleys_avg'] = calculate_peaks_valleys_avg(df, peaks_valleys_aVWAPs, avg_lookback)

    if gaps_avg and gaps_aVWAPs:
        temp_df = pd.DataFrame(gaps_aVWAPs)
        all_aVWAPs['Gaps_avg'] = temp_df.mean(axis=1)
        df['Gaps_avg'] = temp_df.mean(axis=1)

    if OB_avg and OB_aVWAPs:
        temp_df = pd.DataFrame(OB_aVWAPs)
        all_aVWAPs['OB_avg'] = temp_df.mean(axis=1)
        df['OB_avg'] = temp_df.mean(axis=1)

    # Calculate average from all aVWAPs
    if (peaks_valleys_avg or gaps_avg or OB_avg) and (peaks_valleys_aVWAPs or gaps_aVWAPs or OB_aVWAPs):
        temp_df = pd.DataFrame(all_aVWAPs)
        all_aVWAPs['All_avg'] = temp_df.mean(axis=1)
        df['All_avg'] = temp_df.mean(axis=1)

    # Format dataframe --------------------------------------------------------

    cols_to_drop = ['Open', 'Close', 'High', 'Low', 'Volume']
    if peaks_valleys:
        cols_to_drop.extend(['Valleys', 'Peaks'])
    if gaps:
        cols_to_drop.extend(['Gap_Up', 'Gap_Down'])

    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    df.set_index('date', inplace=True)

    # Create final results dictionary -----------------------------------------

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
        result_dict['OB'] = df['OB']
        result_dict['OB_High'] = df['OB_High']
        result_dict['OB_Low'] = df['OB_Low']
        result_dict['OB_Mitigated_Index'] = df['OB_Mitigated_Index']

    # Add averages if calculated
    if peaks_valleys_avg and 'Peaks_Valleys_avg' in df.columns:
        result_dict['Peaks_Valleys_avg'] = df['Peaks_Valleys_avg']
    if gaps_avg and 'Gaps_avg' in df.columns:
        result_dict['Gaps_avg'] = df['Gaps_avg']
    if OB_avg and 'OB_avg' in df.columns:
        result_dict['OB_avg'] = df['OB_avg']
    if 'All_avg' in df.columns:
        result_dict['All_avg'] = df['All_avg']

    return result_dict

def calculate_indicator(df, **params):
    return calculate_avwap_channel(df, **params)

# Utils -----------------------------------------------------------------------

def calculate_avwap(df, anchor_index):
    """Calculate anchored VWAP from anchor point"""
    df_anchored = df.iloc[anchor_index:].copy()
    df_anchored['cumulative_volume'] = df_anchored['Volume'].cumsum()
    df_anchored['cumulative_volume_price'] = (df_anchored['Volume'] * 
        (df_anchored['High'] + df_anchored['Low'] + df_anchored['Close']) / 3).cumsum()
    return df_anchored['cumulative_volume_price'] / df_anchored['cumulative_volume']


def calculate_peaks_valleys_avg(df, peaks_valleys_aVWAPs, avg_lookback=50):
    """
    Bulletproof version that handles all edge cases:
    - Variable aVWAP lengths
    - Missing data
    - Index alignment
    """
    # Convert to DataFrame and sort by anchor recency (newest first)
    aVWAP_df = pd.DataFrame(peaks_valleys_aVWAPs)
    
    # Sort columns by anchor index (newest first)
    sorted_cols = sorted(aVWAP_df.columns, 
                        key=lambda x: int(x.split('_')[-1]), 
                        reverse=True)
    aVWAP_df = aVWAP_df[sorted_cols]
    
    # Initialize output with NaNs matching original DataFrame length
    avg_values = pd.Series(np.nan, index=df.index)
    
    # Process each timestamp that exists in both DataFrames
    common_indices = aVWAP_df.index.intersection(df.index)
    for idx in common_indices:
        # Get last N non-NaN aVWAP values at this timestamp
        valid_vals = aVWAP_df.loc[idx].dropna()[:avg_lookback]
        if len(valid_vals) > 0:
            avg_values.loc[idx] = valid_vals.mean()
    
    return avg_values
