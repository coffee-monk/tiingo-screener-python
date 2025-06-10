import pandas as pd

def StDev(df, threshold=2, mode='oversold'):
    """
    Checks if the most recent price is overbought or oversold based on StDev bands
    
    Parameters:
        df (pd.DataFrame): Must contain:
            - 'StDev_Mean' (centerline)
            - 'Close' (current price)
            - 'StDev' (standard deviation)
        threshold: how many StDevs from the centreline 
        mode: 'oversold' or 'overbought' - which condition to check
            
    Returns:
        pd.DataFrame: Single-row DataFrame of the most recent data if condition met,
                     else empty DataFrame
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    # Get the most recent data
    latest_row = df.iloc[-1]
    
    # Check conditions based on mode
    if mode == 'oversold':
        # Price is significantly below mean (oversold condition)
        if (latest_row['Close'] < (latest_row['StDev_Mean'] - threshold * latest_row['StDev'])):
            return pd.DataFrame([latest_row])
            
    elif mode == 'overbought':
        # Price is significantly above mean (overbought condition)
        if (latest_row['Close'] > (latest_row['StDev_Mean'] + threshold * latest_row['StDev'])):
            return pd.DataFrame([latest_row])
    
    return pd.DataFrame()  # Return empty if condition not met
