import pandas as pd

def supertrend(df, mode='bullish'):
    """
    Combined Supertrend scanner that detects bullish or bearish conditions.
    
    Parameters:
        df (pd.DataFrame): Must contain:
            - 'Supertrend_Direction' (1=bullish, -1=bearish)
        mode (str): Either 'bullish' or 'bearish' to specify scan direction
            
    Returns:
        pd.DataFrame: Single-row DataFrame of current candle if condition met,
                     else empty DataFrame
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]  # Last row (current candle)
    
    # Validate Supertrend_Direction exists and is valid
    if 'Supertrend_Direction' not in latest.index or pd.isna(latest['Supertrend_Direction']):
        return pd.DataFrame()
    
    # Check conditions based on mode
    condition_met = False
    
    if mode.lower() == 'bullish':
        condition_met = (latest['Supertrend_Direction'] == 1)
    elif mode.lower() == 'bearish':
        condition_met = (latest['Supertrend_Direction'] == -1)
    else:
        raise ValueError("mode must be either 'bullish' or 'bearish'")
    
    if condition_met:
        return df.iloc[-1:].copy()  # Return current candle as 1-row dataframe
    
    return pd.DataFrame()  # Return empty if condition not met
