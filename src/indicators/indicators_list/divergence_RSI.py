import pandas as pd
import numpy as np
from typing import Dict

def calculate_rsi_divergence(df: pd.DataFrame, 
                             rsi_period: int = 14,
                             lookback: int = 10) -> Dict[str, pd.Series]:
    """
    Calculates RSI regular and hidden divergences.
    
    Returns:
    {
        'RSI': Raw RSI values,
        'RSI_Regular_Bullish': True at bullish divergence points,
        'RSI_Regular_Bearish': True at bearish divergence points,
        'RSI_Hidden_Bullish': True at hidden bullish points,
        'RSI_Hidden_Bearish': True at hidden bearish points
    }
    """
    results = {}
    
    # 1. Calculate RSI
    results['RSI'] = _calculate_rsi(df['Close'], rsi_period)
    
    # 2. Find peaks and valleys
    price_peaks   = _find_peaks(df['Close'], lookback)
    price_valleys = _find_valleys(df['Close'], lookback)
    rsi_peaks     = _find_peaks(results['RSI'], lookback)
    rsi_valleys   = _find_valleys(results['RSI'], lookback)
    
    # 3. Detect divergences
    results.update({
        'RSI_Regular_Bullish': _detect_bullish_divergence( df['Close'], results['RSI'], price_valleys, rsi_valleys, lookback),
        'RSI_Regular_Bearish': _detect_bearish_divergence( df['Close'], results['RSI'], price_peaks, rsi_peaks, lookback),
        'RSI_Hidden_Bullish':  _detect_hidden_bullish_divergence( df['Close'], results['RSI'], price_valleys, rsi_valleys, lookback),
        'RSI_Hidden_Bearish':  _detect_hidden_bearish_divergence( df['Close'], results['RSI'], price_peaks, rsi_peaks, lookback)
    })
    
    return results

def calculate_indicator(df: pd.DataFrame, **params) -> Dict[str, pd.Series]:
    return calculate_rsi_divergence(df, **params)

# Helper functions ----------------------------------------------------------

def _calculate_rsi(close: pd.Series, period: int) -> pd.Series:
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def _find_peaks(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).max() == series)

def _find_valleys(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).min() == series)

def _detect_bullish_divergence(price: pd.Series, rsi: pd.Series, 
                               price_valleys: pd.Series, rsi_valleys: pd.Series,
                               lookback: int) -> pd.Series:
    return (price_valleys & 
            (price < price.shift(lookback)) & 
            (rsi > rsi.shift(lookback)))

def _detect_bearish_divergence(price: pd.Series, rsi: pd.Series,
                               price_peaks: pd.Series, rsi_peaks: pd.Series,
                               lookback: int) -> pd.Series:
    return (price_peaks & 
            (price > price.shift(lookback)) & 
            (rsi < rsi.shift(lookback)))

def _detect_hidden_bullish_divergence(price: pd.Series, rsi: pd.Series,
                                      price_valleys: pd.Series, rsi_valleys: pd.Series,
                                      lookback: int) -> pd.Series:
    return (price_valleys & 
            (price > price.shift(lookback)) & 
            (rsi < rsi.shift(lookback)))

def _detect_hidden_bearish_divergence(price: pd.Series, rsi: pd.Series,
                                      price_peaks: pd.Series, rsi_peaks: pd.Series,
                                      lookback: int) -> pd.Series:
    return (price_peaks & 
            (price < price.shift(lookback)) & 
            (rsi > rsi.shift(lookback)))

def calculate_indicator(df, **params):
    return calculate_rsi_divergence(df, **params)
