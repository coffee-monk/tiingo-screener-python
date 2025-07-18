import pandas as pd
import numpy as np

def OB_support(df, atr_threshold_multiplier=None):
    """
    Finds bullish Order Blocks with optional ATR tolerance.
    Args:
        df: DataFrame with columns ['Close', 'OB', 'OB_High', 'OB_Low'] (+['ATR'] if using tolerance).
        atr_threshold_multiplier: None for strict mode (original OB range), or float (e.g., 0.5) for ATR-adjusted tolerance.
    Returns:
        pd.DataFrame: Single-row DataFrame of matching OB, or empty if none found.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    current_price = df['Close'].iloc[-1]
    
    # Calculate tolerance if using ATR
    tolerance = 0.0
    if atr_threshold_multiplier is not None:
        if 'ATR' not in df.columns:
            df = df.copy()
            df['ATR'] = calculate_atr(df)
        tolerance = df['ATR'].iloc[-1] * atr_threshold_multiplier
    
    # Search for most recent OB
    for i in range(len(df)-1, -1, -1):
        if df['OB'].iloc[i] == 1:
            ob = df.iloc[i]
            low = ob['OB_Low'] - (tolerance if atr_threshold_multiplier is not None else 0.0)
            high = ob['OB_High'] + (tolerance if atr_threshold_multiplier is not None else 0.0)
            
            if low <= current_price <= high:
                return pd.DataFrame([ob])
            break
    
    return pd.DataFrame()

def calculate_atr(df, length=7):
    """
    Computes Average True Range (ATR) without external libraries.
    Args:
        df: DataFrame with columns ['High', 'Low', 'Close'].
        length: ATR period (default 14).
    Returns:
        pd.Series: ATR values.
    """
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    # True Range calculation
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # ATR (SMA for first 'length' values, then EMA)
    atr = tr.rolling(length).mean()
    atr[length:] = tr.ewm(span=length, adjust=False).mean()[length:]
    return atr
