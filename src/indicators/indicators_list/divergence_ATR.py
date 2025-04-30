import pandas as pd
import numpy as np
from typing import Dict

def calculate_atr_divergence(df: pd.DataFrame, 
                             period: int = 14,
                             lookback: int = 5) -> Dict[str, pd.Series]:
    """
    Calculates ATR (Average True Range) divergences.
    
    Returns:
    {
        'ATR': Raw ATR values,
        'ATR_Regular_Bullish': True at bullish divergence points,
        'ATR_Regular_Bearish': True at bearish divergence points,
        'ATR_Hidden_Bullish': True at hidden bullish points,
        'ATR_Hidden_Bearish': True at hidden bearish points
    }
    """
    results = {}
    
    # 1. Calculate True Range and ATR
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift(1))
    low_close = np.abs(df['Low'] - df['Close'].shift(1))
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    results['ATR'] = tr.rolling(period).mean()
    
    # 2. Find peaks and valleys
    price_peaks = _find_peaks(df['Close'], lookback)
    price_valleys = _find_valleys(df['Close'], lookback)
    atr_peaks = _find_peaks(results['ATR'], lookback)
    atr_valleys = _find_valleys(results['ATR'], lookback)
    
    # 3. Detect divergences
    results.update({
        'ATR_Regular_Bullish': (price_valleys & 
                              (df['Close'] < df['Close'].shift(lookback)) & 
                              (results['ATR'] > results['ATR'].shift(lookback))),
        'ATR_Regular_Bearish': (price_peaks & 
                              (df['Close'] > df['Close'].shift(lookback)) & 
                              (results['ATR'] < results['ATR'].shift(lookback))),
        'ATR_Hidden_Bullish': (price_valleys & 
                             (df['Close'] > df['Close'].shift(lookback)) & 
                             (results['ATR'] < results['ATR'].shift(lookback))),
        'ATR_Hidden_Bearish': (price_peaks & 
                             (df['Close'] < df['Close'].shift(lookback)) & 
                             (results['ATR'] > results['ATR'].shift(lookback)))
    })
    
    return results

# Utility Functions (same as other modules)
def _find_peaks(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).max() == series)

def _find_valleys(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).min() == series)

def calculate_indicator(df, **params):
    return calculate_atr_divergence(df, **params)
