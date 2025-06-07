import pandas as pd

def banker_RSI(df, threshold_lower=1, threshold_upper=20):
    """
    Scan for banker_RSI values within a band (between lower and upper thresholds).
    
    Parameters:
        - threshold_lower (float): Minimum value to trigger (default: 15).
        - threshold_upper (float): Maximum value to trigger (default: 30).
    
    Returns:
        pd.DataFrame: Single-row DataFrame if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    # Check if banker_RSI is within the band
    if (latest['banker_RSI'] > threshold_lower) and (latest['banker_RSI'] < threshold_upper):
        return df.iloc[-1:].copy()  # Return the latest row as a DataFrame
    return pd.DataFrame()
