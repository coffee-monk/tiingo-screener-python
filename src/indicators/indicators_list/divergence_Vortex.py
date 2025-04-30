import pandas as pd
import numpy as np
from typing import Dict

def calculate_vortex_divergence(df: pd.DataFrame, 
                                period: int = 14,
                                lookback: int = 5) -> Dict[str, pd.Series]:
    """
    Calculates Vortex Indicator regular and hidden divergences.
    
    Parameters:
        df: DataFrame with columns ['High', 'Low', 'Close']
        period: Vortex lookback period (default 14)
        lookback: Divergence comparison window (default 5)
    
    Returns:
        Dictionary with:
        - 'VI_plus': Positive vortex movement
        - 'VI_minus': Negative vortex movement 
        - 'VI_Regular_Bullish': Regular bullish divergences
        - 'VI_Regular_Bearish': Regular bearish divergences
        - 'VI_Hidden_Bullish': Hidden bullish divergences
        - 'VI_Hidden_Bearish': Hidden bearish divergences
    """
    
    # 1. Calculate True Range and Vortex Movement
    tr = pd.DataFrame({
        'tr1': df['High'] - df['Low'],
        'tr2': abs(df['High'] - df['Close'].shift(1)),
        'tr3': abs(df['Low'] - df['Close'].shift(1))
    }).max(axis=1)
    
    vm_plus = abs(df['High'] - df['Low'].shift(1))
    vm_minus = abs(df['Low'] - df['High'].shift(1))
    
    # 2. Calculate Vortex Indicators
    results = {
        'VI_plus': vm_plus.rolling(period).sum() / tr.rolling(period).sum(),
        'VI_minus': vm_minus.rolling(period).sum() / tr.rolling(period).sum()
    }
    
    # 3. Find peaks and valleys
    price_peaks = (df['High'].rolling(lookback, center=True).max() == df['High'])
    price_valleys = (df['Low'].rolling(lookback, center=True).min() == df['Low'])
    vi_peaks = (results['VI_plus'].rolling(lookback, center=True).max() == results['VI_plus'])
    vi_valleys = (results['VI_minus'].rolling(lookback, center=True).min() == results['VI_minus'])
    
    # 4. Detect divergences
    results.update({
        'VI_Regular_Bullish': (price_valleys & 
                              (df['Low'] < df['Low'].shift(lookback)) & 
                              (results['VI_minus'] > results['VI_minus'].shift(lookback))),
        'VI_Regular_Bearish': (price_peaks & 
                              (df['High'] > df['High'].shift(lookback)) & 
                              (results['VI_plus'] < results['VI_plus'].shift(lookback))),
        'VI_Hidden_Bullish': (price_valleys & 
                             (df['Low'] > df['Low'].shift(lookback)) & 
                             (results['VI_minus'] < results['VI_minus'].shift(lookback))),
        'VI_Hidden_Bearish': (price_peaks & 
                             (df['High'] < df['High'].shift(lookback)) & 
                             (results['VI_plus'] > results['VI_plus'].shift(lookback)))
    })
    
    return results

def calculate_indicator(df, **params):
    return calculate_vortex_divergence(df, **params)
