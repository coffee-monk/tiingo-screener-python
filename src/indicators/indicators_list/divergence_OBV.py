import pandas as pd
import numpy as np
from typing import Dict

def calculate_obv_divergence(df: pd.DataFrame, 
                             period: int = 21,
                             lookback: int = 5) -> Dict[str, pd.Series]:
    """
    Calculates OBV regular and hidden divergences.
    
    Returns:
    {
        'OBV': Raw OBV values,
        'OBV_Smoothed': Smoothed OBV (EMA),
        'OBV_Regular_Bullish': True at bullish divergence points,
        'OBV_Regular_Bearish': True at bearish divergence points,
        'OBV_Hidden_Bullish': True at hidden bullish points,
        'OBV_Hidden_Bearish': True at hidden bearish points
    }
    """
    results = {}
    
    # 1. Calculate OBV
    obv = [0]
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
            obv.append(obv[-1] + df['Volume'].iloc[i])
        elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
            obv.append(obv[-1] - df['Volume'].iloc[i])
        else:
            obv.append(obv[-1])
    
    results['OBV'] = pd.Series(obv, index=df.index)
    results['OBV_Smoothed'] = results['OBV'].ewm(span=period, adjust=False).mean()
    
    # 2. Find peaks and valleys
    price_peaks = _find_peaks(df['Close'], lookback)
    price_valleys = _find_valleys(df['Close'], lookback)
    obv_peaks = _find_peaks(results['OBV_Smoothed'], lookback)
    obv_valleys = _find_valleys(results['OBV_Smoothed'], lookback)
    
    # 3. Detect divergences
    results.update({
        'OBV_Regular_Bullish': _detect_bullish_divergence(
            df['Close'], results['OBV_Smoothed'], price_valleys, obv_valleys, lookback),
        'OBV_Regular_Bearish': _detect_bearish_divergence(
            df['Close'], results['OBV_Smoothed'], price_peaks, obv_peaks, lookback),
        'OBV_Hidden_Bullish': _detect_hidden_bullish_divergence(
            df['Close'], results['OBV_Smoothed'], price_valleys, obv_valleys, lookback),
        'OBV_Hidden_Bearish': _detect_hidden_bearish_divergence(
            df['Close'], results['OBV_Smoothed'], price_peaks, obv_peaks, lookback)
    })
    
    return results

def _find_peaks(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).max() == series)

def _find_valleys(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).min() == series)

def _detect_bullish_divergence(price: pd.Series, obv: pd.Series, 
                             price_valleys: pd.Series, obv_valleys: pd.Series,
                             lookback: int) -> pd.Series:
    return (price_valleys & 
            (price < price.shift(lookback)) & 
            (obv > obv.shift(lookback)))

def _detect_bearish_divergence(price: pd.Series, obv: pd.Series,
                             price_peaks: pd.Series, obv_peaks: pd.Series,
                             lookback: int) -> pd.Series:
    return (price_peaks & 
            (price > price.shift(lookback)) & 
            (obv < obv.shift(lookback)))

def _detect_hidden_bullish_divergence(price: pd.Series, obv: pd.Series,
                                    price_valleys: pd.Series, obv_valleys: pd.Series,
                                    lookback: int) -> pd.Series:
    return (price_valleys & 
            (price > price.shift(lookback)) & 
            (obv < obv.shift(lookback)))

def _detect_hidden_bearish_divergence(price: pd.Series, obv: pd.Series,
                                    price_peaks: pd.Series, obv_peaks: pd.Series,
                                    lookback: int) -> pd.Series:
    return (price_peaks & 
            (price < price.shift(lookback)) & 
            (obv > obv.shift(lookback)))

def calculate_indicator(df, **params):
    return calculate_obv_divergence(df, **params)
