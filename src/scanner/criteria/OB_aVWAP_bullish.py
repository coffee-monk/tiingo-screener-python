import pandas as pd

def OB_aVWAP_bullish(df):
    """
    Finds the most recent Order Block (looking backward through history) 
    and checks if it's bullish (OB=1).
    
    Parameters:
        df (pd.DataFrame): Must contain 'OB' column with values:
            -1 : Bearish Order Block
            0  : Neutral (no OB)
            1  : Bullish Order Block
            
    Returns:
        pd.DataFrame: Single-row DataFrame of most recent bullish OB if found, 
                     else empty DataFrame
    """
    # Reverse the dataframe to search from most recent to oldest
    reversed_df = df.iloc[::-1]
    
    # Find the first non-zero OB (most recent in actual time)
    recent_OB = reversed_df[reversed_df['OB'] != 0].head(1)
    
    # Check if it's bullish (OB=1)
    if not recent_OB.empty and recent_OB.iloc[0]['OB'] == 1:
        return recent_OB
    return pd.DataFrame()
