import pandas as pd
import numpy as np
from src.indicators.peaks_valleys import calculate_peaks_valleys

def calculate_anchored_vwap(df, anchor_column):
    df['hlc3'] = (df['High'] + df['Low'] + df['Close']) / 3

    vwap_values = []
    cumulative_price_volume = 0.0
    cumulative_volume = 0.0

    for i in range(len(df)):
        if df[anchor_column].iloc[i] == 1.0:  # Check for anchor point (peak or valley)
            cumulative_price_volume = 0.0 # Reset cumulative values at the anchor point
            cumulative_volume = 0.0
        cumulative_price_volume += df['hlc3'].iloc[i] * df['Volume'].iloc[i] # Calculate cumulative price * volume and cumulative volume
        cumulative_volume += df['Volume'].iloc[i]
        if cumulative_volume > 0: # Calculate VWAP for the current row
            vwap = cumulative_price_volume / cumulative_volume
        else:
            vwap = np.nan
        vwap_values.append(vwap)

    return vwap_values

def calculate_indicator(df):

    peaks_valleys = calculate_peaks_valleys(df)
    df['Valleys'] = peaks_valleys['Valleys']
    df['Peaks'] = peaks_valleys['Peaks']
    
    valleys_aVWAP = calculate_anchored_vwap(df, 'Valleys')
    peaks_aVWAP = calculate_anchored_vwap(df, 'Peaks')

    return {
        'Valleys': df['Valleys'],
        'Peaks': df['Peaks'],
        'Valleys_aVWAP': valleys_aVWAP,
        'Peaks_aVWAP': peaks_aVWAP 
    }
