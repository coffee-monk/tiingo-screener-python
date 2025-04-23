import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators

def calculate_avwap(df, anchor_index):
    """Calculate anchored VWAP from anchor point"""
    df_anchored = df.iloc[anchor_index:].copy()
    df_anchored['cumulative_volume'] = df_anchored['Volume'].cumsum()
    df_anchored['cumulative_volume_price'] = (df_anchored['Volume'] * 
        (df_anchored['High'] + df_anchored['Low'] + df_anchored['Close']) / 3).cumsum()
    return df_anchored['cumulative_volume_price'] / df_anchored['cumulative_volume']

def calculate_avwap_channel(df, peaks_valleys=True, aVWAP_avg=True, gaps=False, gaps_avg=False, window_size=200):
    # Get indicators based on parameters
    aVWAP_anchors = []
    if peaks_valleys or aVWAP_avg:
        aVWAP_anchors.append('peaks_valleys')
    if gaps or gaps_avg:
        aVWAP_anchors.append('gaps')
 
    if not aVWAP_anchors:  # If no anchor types selected
        return {}
 
    params = {}
    if peaks_valleys:
        params['peaks_valleys'] = {'window_size': window_size}
    if gaps:
        params['gaps'] = {}  # Add gap parameters if needed
 
    df = get_indicators(df, aVWAP_anchors, params)
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])

    # Initialize separate dictionaries for peaks/valleys and gaps
    peaks_valleys_aVWAPs = {}
    gaps_aVWAPs = {}

    # Calculate peaks/valleys aVWAPs if requested
    if peaks_valleys or aVWAP_avg:
        peaks_indices = df[df['Peaks'] == 1].index.tolist() if 'Peaks' in df.columns else []
        valleys_indices = df[df['Valleys'] == 1].index.tolist() if 'Valleys' in df.columns else []
     
        for i in peaks_indices:
            peaks_valleys_aVWAPs[f'aVWAP_{i}'] = calculate_avwap(df, i)
        for i in valleys_indices:
            peaks_valleys_aVWAPs[f'aVWAP_{i}'] = calculate_avwap(df, i)

    # Calculate gaps aVWAPs if requested
    if gaps or gaps_avg:
        gap_up_indices = df[df['Gap_Up'] == 1].index.tolist() if 'Gap_Up' in df.columns else []
        gap_down_indices = df[df['Gap_Down'] == 1].index.tolist() if 'Gap_Down' in df.columns else []
     
        for i in gap_up_indices:
            gaps_aVWAPs[f'Gap_aVWAP_{i}'] = calculate_avwap(df, i)
        for i in gap_down_indices:
            gaps_aVWAPs[f'Gap_aVWAP_{i}'] = calculate_avwap(df, i)

    # Combine all aVWAPs
    all_aVWAPs = {**peaks_valleys_aVWAPs, **gaps_aVWAPs}
 
    if not all_aVWAPs:  # If no anchor points found
        return {}
 
    # Add all aVWAP columns to dataframe
    df = pd.concat([df, pd.DataFrame(all_aVWAPs)], axis=1)

    # Calculate averages if requested
    if aVWAP_avg and peaks_valleys_aVWAPs:
        # Calculate average from peaks/valleys aVWAPs
        temp_df = pd.DataFrame(peaks_valleys_aVWAPs)
        all_aVWAPs['aVWAP_avg'] = temp_df.mean(axis=1)
        df['aVWAP_avg'] = temp_df.mean(axis=1)
 
    if gaps_avg and gaps_aVWAPs:
        # Calculate average from gap aVWAPs
        temp_df = pd.DataFrame(gaps_aVWAPs)
        all_aVWAPs['Gap_aVWAP_avg'] = temp_df.mean(axis=1)
        df['Gap_aVWAP_avg'] = temp_df.mean(axis=1)
 
    if (aVWAP_avg or gaps_avg) and (peaks_valleys_aVWAPs or gaps_aVWAPs):
        # Calculate average from all aVWAPs
        temp_df = pd.DataFrame(all_aVWAPs)
        all_aVWAPs['All_aVWAP_avg'] = temp_df.mean(axis=1)
        df['All_aVWAP_avg'] = temp_df.mean(axis=1)

    # Clean up dataframe
    cols_to_drop = ['Open', 'Close', 'High', 'Low', 'Volume']
    if peaks_valleys:
        cols_to_drop.extend(['Valleys', 'Peaks'])
    if gaps:
        cols_to_drop.extend(['Gap_Up', 'Gap_Down'])
 
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    df.set_index('date', inplace=True)

    # Create final output dictionary
    result_dict = {}
 
    # Add peaks/valleys aVWAPs if they exist
    if peaks_valleys and peaks_valleys_aVWAPs:
        for col in peaks_valleys_aVWAPs:
            result_dict[col] = df[col]
 
    # Add gaps aVWAPs if they exist
    if gaps and gaps_aVWAPs:
        for col in gaps_aVWAPs:
            result_dict[col] = df[col]
 
    # Add averages if calculated
    if aVWAP_avg and 'aVWAP_avg' in df.columns:
        result_dict['aVWAP_avg'] = df['aVWAP_avg']
    if gaps_avg and 'Gap_aVWAP_avg' in df.columns:
        result_dict['Gap_aVWAP_avg'] = df['Gap_aVWAP_avg']
    if 'All_aVWAP_avg' in df.columns:
        result_dict['All_aVWAP_avg'] = df['All_aVWAP_avg']
 
    return result_dict

def calculate_indicator(df, **params):
    return calculate_avwap_channel(df, **params)
