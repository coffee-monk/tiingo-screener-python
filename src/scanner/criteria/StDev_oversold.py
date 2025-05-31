import pandas as pd

def StDev_oversold(df):
    """
    Checks if the most recent StDev is oversold (price is significantly below mean)
    
    Parameters:
        df (pd.DataFrame): Must contain:
            - 'StDev_Mean' (centerline)
            - 'Close' (current price)
            - 'StDev' (standard deviation)
            
    Returns:
        pd.DataFrame: Single-row DataFrame of the most recent data if condition met,
                     else empty DataFrame
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    # Get the most recent data
    latest_row = df.iloc[-1]
    
    # Check if price is significantly below mean (oversold condition)
    # Using 2 standard deviations as threshold
    if (latest_row['Close'] < (latest_row['StDev_Mean'] - 1 * latest_row['StDev'])):
        return pd.DataFrame([latest_row])  # Return the latest row as DataFrame
    
    return pd.DataFrame()  # Return empty if condition not met
