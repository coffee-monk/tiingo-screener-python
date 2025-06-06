import pandas as pd

def supertrend_bearish(df):
    """
    Checks if the most recent Supertrend direction is bearish (-1).
    
    Parameters:
        df (pd.DataFrame): Must contain:
            - 'Supertrend_Direction' (1=bullish, -1=bearish)
            
    Returns:
        pd.DataFrame: Single-row DataFrame of current candle if bearish,
                     else empty DataFrame
    """
    latest = df.iloc[-1]  # Last row (current candle)
    
    if latest['Supertrend_Direction'] == -1:
        return df.iloc[-1:].copy()  # Return current candle as 1-row dataframe
    
    return pd.DataFrame()  # Return empty if not bearish
