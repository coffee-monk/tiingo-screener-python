import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators


def calculate_zscore_probability(df, lookback=75, centreline="OB_avg"):
    # centreline options: "peaks_valleys_avg", "gaps_avg", "OB_avg"
    # defaults to 75 period SMA 

    if centreline == 'peaks_valleys_avg':
        df = get_indicators(df, ['aVWAP'], {'aVWAP': {'peaks_valleys_avg': True}})
        aVWAP_mean = df['Peaks_Valleys_avg']
        price_deviation = df['Close'] - aVWAP_mean
        aVWAP_std = price_deviation.rolling(window=lookback).std()
        z_score = (df['Close'] - aVWAP_mean) / aVWAP_std

    elif centreline == 'OB_avg':
        df = get_indicators(df, ['aVWAP'], {'aVWAP': {'OB_avg': True}})
        aVWAP_mean = df['OB_avg']
        price_deviation = df['Close'] - aVWAP_mean
        aVWAP_std = price_deviation.rolling(window=lookback).std()
        z_score = (df['Close'] - aVWAP_mean) / aVWAP_std

    elif centreline == 'gaps_avg':
        df = get_indicators(df, ['aVWAP'], {'aVWAP': {'gaps_avg': True}})
        aVWAP_mean = df['Gaps_avg']
        price_deviation = df['Close'] - aVWAP_mean
        aVWAP_std = price_deviation.rolling(window=lookback).std()
        z_score = (df['Close'] - aVWAP_mean) / aVWAP_std

    elif centreline == 'SMA':
        df = get_indicators(df, ['SMA'], {'SMA': {'periods': [lookback]}})
        aVWAP_mean = df[f"SMA_{str(lookback)}"]
        price_deviation = df['Close'] - aVWAP_mean
        aVWAP_std = price_deviation.rolling(window=lookback).std()
        z_score = (df['Close'] - aVWAP_mean) / aVWAP_std

    return {
        'ZScore': z_score,
    }

def calculate_indicator(df, **params):
    return calculate_zscore_probability(df, **params)
