import pandas as pd
import numpy as np
from typing import Dict

def calculate_macd_divergence(df: pd.DataFrame, 
                              fast_period: int = 12,
                              slow_period: int = 26,
                              signal_period: int = 9,
                              lookback: int = 5) -> Dict[str, pd.Series]:
    """
    Calculates MACD regular and hidden divergences.
    
    Returns:
    {
        'MACD': MACD line,
        'Signal': Signal line,
        'Histogram': MACD histogram,
        'MACD_Regular_Bullish': True at bullish divergence points,
        'MACD_Regular_Bearish': True at bearish divergence points,
        'MACD_Hidden_Bullish': True at hidden bullish points,
        'MACD_Hidden_Bearish': True at hidden bearish points
    }
    """
    results = {}
    
    # 1. Calculate MACD
    exp1 = df['Close'].ewm(span=fast_period, adjust=False).mean()
    exp2 = df['Close'].ewm(span=slow_period, adjust=False).mean()
    results['MACD']      = macd = exp1 - exp2
    results['Signal']    = signal = macd.ewm(span=signal_period, adjust=False).mean()
    results['Histogram'] = macd - signal
    
    # 2. Find peaks and valleys
    price_peaks   = _find_peaks(df['Close'], lookback)
    price_valleys = _find_valleys(df['Close'], lookback)
    macd_peaks    = _find_peaks(macd, lookback)
    macd_valleys  = _find_valleys(macd, lookback)
    
    # 3. Detect divergences
    results.update({
        'MACD_Regular_Bullish': _detect_bullish_divergence(
            df['Close'], macd, price_valleys, macd_valleys, lookback),
        'MACD_Regular_Bearish': _detect_bearish_divergence(
            df['Close'], macd, price_peaks, macd_peaks, lookback),
        'MACD_Hidden_Bullish': _detect_hidden_bullish_divergence(
            df['Close'], macd, price_valleys, macd_valleys, lookback),
        'MACD_Hidden_Bearish': _detect_hidden_bearish_divergence(
            df['Close'], macd, price_peaks, macd_peaks, lookback)
    })
    
    return results

def _find_peaks(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).max() == series)

def _find_valleys(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).min() == series)

def _detect_bullish_divergence(price: pd.Series, macd: pd.Series, 
                              price_valleys: pd.Series, macd_valleys: pd.Series,
                              lookback: int) -> pd.Series:
    return (price_valleys & 
            (price < price.shift(lookback)) & 
            (macd > macd.shift(lookback)))

def _detect_bearish_divergence(price: pd.Series, macd: pd.Series,
                              price_peaks: pd.Series, macd_peaks: pd.Series,
                              lookback: int) -> pd.Series:
    return (price_peaks & 
            (price > price.shift(lookback)) & 
            (macd < macd.shift(lookback)))

def _detect_hidden_bullish_divergence(price: pd.Series, macd: pd.Series,
                                     price_valleys: pd.Series, macd_valleys: pd.Series,
                                     lookback: int) -> pd.Series:
    return (price_valleys & 
            (price > price.shift(lookback)) & 
            (macd < macd.shift(lookback)))

def _detect_hidden_bearish_divergence(price: pd.Series, macd: pd.Series,
                                     price_peaks: pd.Series, macd_peaks: pd.Series,
                                     lookback: int) -> pd.Series:
    return (price_peaks & 
            (price < price.shift(lookback)) & 
            (macd > macd.shift(lookback)))

def calculate_indicator(df, **params):
    return calculate_macd_divergence(df, **params)
