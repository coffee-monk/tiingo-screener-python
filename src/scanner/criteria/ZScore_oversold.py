import pandas as pd

def ZScore_oversold(df):
    """
    Checks if the most recent ZScore is below -2 (indicating potential oversold condition).
    
    Parameters:
        df (pd.DataFrame): Must contain 'ZScore' column.
            
    Returns:
        pd.DataFrame: Single-row DataFrame of the most recent data if ZScore < -2,
                     else empty DataFrame
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    # Get the most recent ZScore value
    latest_row = df.iloc[-1]
    
    # Check if ZScore is below -2
    if latest_row['ZScore'] < -2:
        return pd.DataFrame([latest_row])  # Return the latest row as DataFrame
    
    return pd.DataFrame()  # Return empty if condition not met
