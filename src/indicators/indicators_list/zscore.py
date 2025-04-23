import pandas as pd
import numpy as np
from scipy.stats import norm

def calculate_zscore_probability(df, lookback=75, sma_length=75):
    close_sma = df['Close'].rolling(window=lookback).mean()
    close_std = df['Close'].rolling(window=lookback).std()
    
    z_score = (df['Close'] - close_sma) / close_std
    z_score_high = (df['High'] - df['High'].rolling(window=lookback).mean()) / df['High'].rolling(window=lookback).std()
    z_score_low = (df['Low'] - df['Low'].rolling(window=lookback).mean()) / df['Low'].rolling(window=lookback).std()
    z_score_open = (df['Open'] - df['Open'].rolling(window=lookback).mean()) / df['Open'].rolling(window=lookback).std()
    
    # Calculate SMA of Z-Scores
    z_sma = z_score.rolling(window=sma_length).mean()
    
    return {
        'ZScore': z_score,
        'ZScore_SMA': z_sma,
    }

def calculate_indicator(df, **params):
    return calculate_zscore_probability(df, **params)
