import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators

def calculate_zscore_probability(df, lookback=75, aVWAP_avg=True):

    if aVWAP_avg and 'OB_avg' in df.columns:
        df = get_indicators(df, ['aVWAP'])
        # Calculate rolling StdDev of price deviations from aVWAP mean
        aVWAP_mean = df['OB_avg']
        price_deviation = df['Close'] - aVWAP_mean
        aVWAP_std = price_deviation.rolling(window=lookback).std()
        z_score = (df['Close'] - aVWAP_mean) / aVWAP_std
    else:
        close_sma = df['Close'].rolling(window=lookback).mean()
        close_std = df['Close'].rolling(window=lookback).std()
        z_score = (df['Close'] - close_sma) / close_std
        
    return {
        'ZScore': z_score,
    }

def calculate_indicator(df, **params):
    return calculate_zscore_probability(df, **params)
