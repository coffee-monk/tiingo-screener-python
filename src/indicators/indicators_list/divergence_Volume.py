import pandas as pd
import numpy as np
from typing import Dict

def calculate_volume_divergence(df: pd.DataFrame, 
                                period: int = 14,
                                lookback: int = 5) -> Dict[str, pd.Series]:
    """
    Calculates volume divergences - detects when price moves lack volume support.
    
    Returns:
    {
        'Volume_MA': Smoothed volume (EMA),
        'Vol_Regular_Bullish': Price low + volume higher low,
        'Vol_Regular_Bearish': Price high + volume lower high,
        'Vol_Hidden_Bullish': Price higher low + volume lower low,
        'Vol_Hidden_Bearish': Price lower high + volume higher high
    }
    """
    results = {}
    
    # 1. Calculate smoothed volume
    results['Volume_MA'] = df['Volume'].ewm(span=period, adjust=False).mean()
    
    # 2. Find peaks/valleys in price and volume
    price_peaks = _find_peaks(df['Close'], lookback)
    price_valleys = _find_valleys(df['Close'], lookback)
    vol_peaks = _find_peaks(results['Volume_MA'], lookback)
    vol_valleys = _find_valleys(results['Volume_MA'], lookback)
    
    # 3. Detect divergences
    results.update({
        'Vol_Regular_Bullish': (price_valleys & 
                              (df['Close'] < df['Close'].shift(lookback)) & 
                              (results['Volume_MA'] > results['Volume_MA'].shift(lookback))),
        
        'Vol_Regular_Bearish': (price_peaks & 
                              (df['Close'] > df['Close'].shift(lookback)) & 
                              (results['Volume_MA'] < results['Volume_MA'].shift(lookback))),
        
        'Vol_Hidden_Bullish': (price_valleys & 
                             (df['Close'] > df['Close'].shift(lookback)) & 
                             (results['Volume_MA'] < results['Volume_MA'].shift(lookback))),
        
        'Vol_Hidden_Bearish': (price_peaks & 
                             (df['Close'] < df['Close'].shift(lookback)) & 
                             (results['Volume_MA'] > results['Volume_MA'].shift(lookback)))
    })
    
    return results

# Reused Utility Functions (same as momentum module)
def _find_peaks(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).max() == series)

def _find_valleys(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).min() == series)

def calculate_indicator(df, **params):
    return calculate_volume_divergence(df, **params)
