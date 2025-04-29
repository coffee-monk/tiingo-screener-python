import pandas as pd
import numpy as np

def calculate_ema(series, window):
    """Calculate Exponential Moving Average"""
    return series.ewm(span=window, adjust=False).mean()

def calculate_atr(high, low, close, window=14):
    """Calculate Average True Range"""
    tr = pd.DataFrame({
        'hl': high - low,
        'hc': abs(high - close.shift(1)),
        'lc': abs(low - close.shift(1))
    }).max(axis=1)
    return tr.rolling(window).mean()

def calculate_wae(df, 
                fast_period=20, 
                slow_period=40, 
                atr_period=20,
                explosion_multiplier=2.0):
    """
    Pure Python Waddah Attar Explosion Implementation
    
    Parameters:
        df : DataFrame with columns ['Open','High','Low','Close']
        fast_period : Fast EMA period (default 20)
        slow_period : Slow EMA period (default 40)
        atr_period : ATR period (default 20)
        explosion_multiplier : ATR multiplier (default 2.0)
    
    Returns:
        DataFrame with columns:
        - WAE_Trend : Directional momentum (-1 to 1)
        - WAE_Momentum : Absolute momentum strength (0+)
        - WAE_Upper : Upper explosion line
        - WAE_Lower : Lower explosion line
    """
    
    close = df['Close']
    high  = df['High']
    low   = df['Low']
    
    # 1. Calculate MACD components
    fast_ema = calculate_ema(close, fast_period)
    slow_ema = calculate_ema(close, slow_period)
    macd_line = fast_ema - slow_ema
    signal_line = calculate_ema(macd_line, 9)  # Standard MACD signal
    
    # 2. Determine trend direction and momentum
    trend_direction = np.where(macd_line > signal_line, 1, -1)
    momentum = (macd_line - signal_line).abs() * 150  # Scaled histogram
    
    # 3. Calculate volatility bands
    atr = calculate_atr(high, low, close, atr_period)
    upper_band = atr * explosion_multiplier
    lower_band = -upper_band
    
    return {
        'WAE_Direction': trend_direction,
        'WAE_Momentum': momentum,
        'WAE_Upper': upper_band,
        'WAE_Lower': lower_band
    }

def calculate_indicator(df, **params):
    return calculate_wae(df, **params)
