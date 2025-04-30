import pandas as pd
import numpy as np
from typing import Dict

def calculate_fisher_divergence(df: pd.DataFrame, 
                                period: int = 10,
                                lookback: int = 5) -> Dict[str, pd.Series]:
    """
    Calculates Fisher Transform regular and hidden divergences.
    
    Returns:
    {
        'Fisher': Fisher Transform values,
        'Fisher_Signal': Smoothed Fisher line,
        'Fisher_Regular_Bullish': True at bullish divergence points,
        'Fisher_Regular_Bearish': True at bearish divergence points,
        'Fisher_Hidden_Bullish': True at hidden bullish points,
        'Fisher_Hidden_Bearish': True at hidden bearish points
    }
    """
    results = {}
    
    # 1. Calculate Fisher Transform
    hl2 = (df['High'] + df['Low']) / 2  # Typical price
    max_hl2 = hl2.rolling(period).max()
    min_hl2 = hl2.rolling(period).min()
    
    # Normalize and smooth
    val = 0.33 * 2 * ((hl2 - min_hl2) / (max_hl2 - min_hl2 + 1e-7) - 0.5)
    val = val.clip(-0.999, 0.999)  # Avoid infinity in log calculation
    
    results['Fisher'] = fisher = 0.5 * np.log((1 + val) / (1 - val))
    results['Fisher_Signal'] = fisher.ewm(span=3, adjust=False).mean()  # Signal line
    
    # 2. Find peaks and valleys (using smoothed Fisher)
    price_peaks = _find_peaks(df['Close'], lookback)
    price_valleys = _find_valleys(df['Close'], lookback)
    fisher_peaks = _find_peaks(results['Fisher'], lookback)
    fisher_valleys = _find_valleys(results['Fisher'], lookback)
    
    # 3. Detect divergences
    results.update({
        'Fisher_Regular_Bullish': _detect_bullish_divergence(
            df['Close'], results['Fisher'], price_valleys, fisher_valleys, lookback),
        'Fisher_Regular_Bearish': _detect_bearish_divergence(
            df['Close'], results['Fisher'], price_peaks, fisher_peaks, lookback),
        'Fisher_Hidden_Bullish': _detect_hidden_bullish_divergence(
            df['Close'], results['Fisher'], price_valleys, fisher_valleys, lookback),
        'Fisher_Hidden_Bearish': _detect_hidden_bearish_divergence(
            df['Close'], results['Fisher'], price_peaks, fisher_peaks, lookback)
    })
    
    return results

def _find_peaks(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).max() == series)

def _find_valleys(series: pd.Series, lookback: int) -> pd.Series:
    return (series.rolling(lookback, center=True).min() == series)

def _detect_bullish_divergence(price: pd.Series, fisher: pd.Series, 
                              price_valleys: pd.Series, fisher_valleys: pd.Series,
                              lookback: int) -> pd.Series:
    return (price_valleys & 
            (price < price.shift(lookback)) & 
            (fisher > fisher.shift(lookback)))

def _detect_bearish_divergence(price: pd.Series, fisher: pd.Series,
                              price_peaks: pd.Series, fisher_peaks: pd.Series,
                              lookback: int) -> pd.Series:
    return (price_peaks & 
            (price > price.shift(lookback)) & 
            (fisher < fisher.shift(lookback)))

def _detect_hidden_bullish_divergence(price: pd.Series, fisher: pd.Series,
                                    price_valleys: pd.Series, fisher_valleys: pd.Series,
                                    lookback: int) -> pd.Series:
    return (price_valleys & 
            (price > price.shift(lookback)) & 
            (fisher < fisher.shift(lookback)))

def _detect_hidden_bearish_divergence(price: pd.Series, fisher: pd.Series,
                                    price_peaks: pd.Series, fisher_peaks: pd.Series,
                                    lookback: int) -> pd.Series:
    return (price_peaks & 
            (price < price.shift(lookback)) & 
            (fisher > fisher.shift(lookback)))

def calculate_indicator(df, **params):
    return calculate_fisher_divergence(df, **params)
