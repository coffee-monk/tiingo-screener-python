import pandas as pd
import numpy as np
from typing import Dict

def calculate_stochastic_divergence(df: pd.DataFrame,
                                  k_period: int = 14,
                                  d_period: int = 3,
                                  lookback: int = 5) -> Dict[str, pd.Series]:
    """
    Calculates Stochastic Oscillator and detects regular/hidden divergences.
    
    Parameters:
        df: DataFrame with OHLCV data
        k_period: %K period (default 14)
        d_period: %D period (default 3)
        lookback: Lookback period for peak/valley detection (default 5)
        
    Returns:
        {
            'Stoch_%K': %K values,
            'Stoch_%D': %D values,
            'Stoch_Regular_Bullish': True at regular bullish divergence points,
            'Stoch_Regular_Bearish': True at regular bearish divergence points,
            'Stoch_Hidden_Bullish': True at hidden bullish divergence points,
            'Stoch_Hidden_Bearish': True at hidden bearish divergence points
        }
    """
    results = {}
    
    # 1. Calculate Stochastic Oscillator (%K and %D)
    low_min = df['Low'].rolling(k_period).min()
    high_max = df['High'].rolling(k_period).max()
    
    results['Stoch_%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    results['Stoch_%D'] = results['Stoch_%K'].rolling(d_period).mean()
    
    # 2. Find price and stochastic peaks/valleys
    price_peaks = _find_peaks(df['Close'], lookback)
    price_valleys = _find_valleys(df['Close'], lookback)
    stoch_peaks = _find_peaks(results['Stoch_%K'], lookback)
    stoch_valleys = _find_valleys(results['Stoch_%K'], lookback)
    
    # 3. Detect divergences
    results.update({
        'Stochastic_Regular_Bullish': (price_valleys & 
                                (df['Close'] < df['Close'].shift(lookback)) & 
                                (results['Stoch_%K'] > results['Stoch_%K'].shift(lookback))),
        'Stochastic_Regular_Bearish': (price_peaks & 
                                (df['Close'] > df['Close'].shift(lookback)) & 
                                (results['Stoch_%K'] < results['Stoch_%K'].shift(lookback))),
        'Stochastic_Hidden_Bullish': (price_valleys & 
                               (df['Close'] > df['Close'].shift(lookback)) & 
                               (results['Stoch_%K'] < results['Stoch_%K'].shift(lookback))),
        'Stochastic_Hidden_Bearish': (price_peaks & 
                               (df['Close'] < df['Close'].shift(lookback)) & 
                               (results['Stoch_%K'] > results['Stoch_%K'].shift(lookback)))
    })
    
    return results

# Utility Functions
def _find_peaks(series: pd.Series, lookback: int) -> pd.Series:
    """Identify peaks in a series using rolling window"""
    return (series.rolling(lookback, center=True).max() == series) & (series.notna())

def _find_valleys(series: pd.Series, lookback: int) -> pd.Series:
    """Identify valleys in a series using rolling window"""
    return (series.rolling(lookback, center=True).min() == series) & (series.notna())

def calculate_indicator(df, **params):
    """Wrapper function for consistent interface"""
    return calculate_stochastic_divergence(df, **params)

def calculate_indicator(df, **params):
    return calculate_stochastic_divergence(df, **params)
