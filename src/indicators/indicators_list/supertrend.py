import pandas as pd
import numpy as np

def calculate_supertrend(df, periods=14, multiplier=3, **params):
    """
    Calculate Supertrend indicator with both upper and lower bands.
    
    Parameters:
        df (pd.DataFrame): DataFrame with OHLC price data
        periods (int): ATR periods (default: 10)
        multiplier (float): ATR multiplier (default: 3)
        **params: Additional parameters
        
    Returns:
        dict: {
            'Supertrend_Upper': upper band values,
            'Supertrend_Lower': lower band values,
            'Supertrend_Direction': directions (1=uptrend, -1=downtrend)
        }
    """
    # Calculate True Range and ATR
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=periods).mean().fillna(0)
    
    # Calculate basic bands
    hl2 = (df['High'] + df['Low']) / 2
    upper_band = hl2 + (multiplier * atr)
    lower_band = hl2 - (multiplier * atr)
    
    # Initialize series
    final_upper = pd.Series(index=df.index, dtype=float)
    final_lower = pd.Series(index=df.index, dtype=float)
    direction = pd.Series(1, index=df.index)  # Default to uptrend
    
    # First values
    final_upper.iloc[0] = upper_band.iloc[0]
    final_lower.iloc[0] = lower_band.iloc[0]
    
    # Calculate subsequent values
    for i in range(1, len(df)):
        # Current bands
        curr_upper = upper_band.iloc[i]
        curr_lower = lower_band.iloc[i]
        
        # Previous values
        prev_upper = final_upper.iloc[i-1]
        prev_lower = final_lower.iloc[i-1]
        prev_close = df['Close'].iloc[i-1]
        
        # Determine current direction
        if prev_close > prev_upper:
            direction.iloc[i] = 1
        elif prev_close < prev_lower:
            direction.iloc[i] = -1
        else:
            direction.iloc[i] = direction.iloc[i-1]
        
        # Calculate final bands
        if direction.iloc[i] == 1:
            final_lower.iloc[i] = max(curr_lower, prev_lower)
            final_upper.iloc[i] = curr_upper
        else:
            final_upper.iloc[i] = min(curr_upper, prev_upper)
            final_lower.iloc[i] = curr_lower
        
        # Check for crossover
        current_close = df['Close'].iloc[i]
        if (direction.iloc[i] == 1 and current_close < final_lower.iloc[i]) or \
           (direction.iloc[i] == -1 and current_close > final_upper.iloc[i]):
            direction.iloc[i] *= -1
            if direction.iloc[i] == 1:
                final_lower.iloc[i] = max(curr_lower, prev_lower)
            else:
                final_upper.iloc[i] = min(curr_upper, prev_upper)
    
    return {
        'Supertrend_Upper': final_upper,
        'Supertrend_Lower': final_lower,
        'Supertrend_Direction': direction
    }

def calculate_indicator(df, **params):
    return calculate_supertrend(df, **params)
