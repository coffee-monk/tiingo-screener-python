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

def calculate_avwap_channel(df, aVWAP_anchor_indices=['peaks_valleys'], window_size=200):
    """
    Calculate anchored VWAP channels and return as dictionary of Series.
    Returns dictionary with keys like 'aVWAP_123' (for anchor at index 123) and 'aVWAP_avg'.
    """
    # Get peaks/valleys indicators first
    df = get_indicators(df, aVWAP_anchor_indices, {'peaks_valleys': {'window_size': window_size}})
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])

    # Find anchor points
    anchor_indices = []
    
    if 'Peaks' in df.columns:
        anchor_indices.extend(df[df['Peaks'] == 1].index.tolist())
    if 'Valleys' in df.columns:
        anchor_indices.extend(df[df['Valleys'] == 1].index.tolist())
    if 'Gap_Up' in df.columns:
        anchor_indices.extend(df[df['Gap_Up'] == 1].index.tolist())
    if 'Gap_Down' in df.columns:
        anchor_indices.extend(df[df['Gap_Down'] == 1].index.tolist())

    # Calculate aVWAPs for each anchor point
    aVWAP_columns = {}
    for i in anchor_indices:
        aVWAP_columns[f'aVWAP_{i}'] = calculate_avwap(df, i)
    df = pd.concat([df, pd.DataFrame(aVWAP_columns)], axis=1)

    # Calculate average if we have aVWAP columns
    if aVWAP_columns:
        # Combine all aVWAP series into a temporary dataframe for averaging
        temp_df = pd.DataFrame(aVWAP_columns)
        aVWAP_columns['aVWAP_avg'] = temp_df.mean(axis=1)
        df['aVWAP_avg'] = temp_df.mean(axis=1)

    df = df.drop(columns=['Open', 'Close', 'High', 'Low', 'Volume', 'Valleys', 'Peaks']) 
    df.set_index('date', inplace=True) 

    avwap_cols = [col for col in df.columns if col.startswith('aVWAP_')]
    avwap_dict = {col: df[col] for col in avwap_cols}

    return avwap_dict

def calculate_indicator(df, **params):
    return calculate_avwap_channel(df, **params)
