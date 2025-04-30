import pandas as pd
import numpy as np
from typing import Dict

def calculate_momentum_divergence(df: pd.DataFrame, 
                                  lookback: int = 5,
                                  smooth_period: int = 3) -> Dict[str, pd.Series]:
    """
    Calculates momentum divergences with columns ready for visualization.
    
    Returns:
    {
        'Momentum': Raw momentum values,
        'Momentum_Smoothed': Smoothed momentum line,
        'Momo_Regular_Bullish': Regular bullish divergences,
        'Momo_Regular_Bearish': Regular bearish divergences,
        'Momo_Hidden_Bullish': Hidden bullish divergences,
        'Momo_Hidden_Bearish': Hidden bearish divergences
    }
    """
    results = {}
    
    # 1. Calculate raw momentum (price change over lookback period)
    results['Momentum'] = df['Close'] - df['Close'].shift(lookback)
    
    # 2. Optional smoothing (3-period EMA by default)
    results['Momentum_Smoothed'] = results['Momentum'].ewm(span=smooth_period, adjust=False).mean()
    
    # 3. Find peaks and valleys in price and momentum
    price_peaks = _find_peaks(df['Close'], lookback)
    price_valleys = _find_valleys(df['Close'], lookback)
    momo_peaks = _find_peaks(results['Momentum'], lookback)
    momo_valleys = _find_valleys(results['Momentum'], lookback)
    
    # 4. Detect all divergence types
    results.update({
        'Momo_Regular_Bullish': _detect_bullish_divergence(
            df['Close'], results['Momentum'], price_valleys, momo_valleys, lookback),
        'Momo_Regular_Bearish': _detect_bearish_divergence(
            df['Close'], results['Momentum'], price_peaks, momo_peaks, lookback),
        'Momo_Hidden_Bullish': _detect_hidden_bullish_divergence(
            df['Close'], results['Momentum'], price_valleys, momo_valleys, lookback),
        'Momo_Hidden_Bearish': _detect_hidden_bearish_divergence(
            df['Close'], results['Momentum'], price_peaks, momo_peaks, lookback)
    })
    
    return results

# Utility Functions
def _find_peaks(series: pd.Series, lookback: int) -> pd.Series:
    """Identifies peaks using centered rolling window"""
    return (series.rolling(lookback, center=True).max() == series)

def _find_valleys(series: pd.Series, lookback: int) -> pd.Series:
    """Identifies valleys using centered rolling window"""
    return (series.rolling(lookback, center=True).min() == series)

def _detect_bullish_divergence(price: pd.Series, momentum: pd.Series,
                              price_valleys: pd.Series, momo_valleys: pd.Series,
                              lookback: int) -> pd.Series:
    """Regular bullish: Lower price lows + higher momentum lows"""
    return (price_valleys & 
            (price < price.shift(lookback)) & 
            (momentum > momentum.shift(lookback)))

def _detect_bearish_divergence(price: pd.Series, momentum: pd.Series,
                              price_peaks: pd.Series, momo_peaks: pd.Series,
                              lookback: int) -> pd.Series:
    """Regular bearish: Higher price highs + lower momentum highs"""
    return (price_peaks & 
            (price > price.shift(lookback)) & 
            (momentum < momentum.shift(lookback)))

def _detect_hidden_bullish_divergence(price: pd.Series, momentum: pd.Series,
                                     price_valleys: pd.Series, momo_valleys: pd.Series,
                                     lookback: int) -> pd.Series:
    """Hidden bullish: Higher price lows + lower momentum lows"""
    return (price_valleys & 
            (price > price.shift(lookback)) & 
            (momentum < momentum.shift(lookback)))

def _detect_hidden_bearish_divergence(price: pd.Series, momentum: pd.Series,
                                     price_peaks: pd.Series, momo_peaks: pd.Series,
                                     lookback: int) -> pd.Series:
    """Hidden bearish: Lower price highs + higher momentum highs"""
    return (price_peaks & 
            (price < price.shift(lookback)) & 
            (momentum > momentum.shift(lookback)))

def calculate_indicator(df, **params):
    return calculate_momentum_divergence(df, **params)

