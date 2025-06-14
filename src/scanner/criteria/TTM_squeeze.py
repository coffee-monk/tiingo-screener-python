import pandas as pd

def TTM_squeeze(df, mode='active'):
    """
    Checks for TTM Squeeze conditions in the most recent price data
    
    Parameters:
        df (pd.DataFrame): Must contain:
            - 'TTM_squeeze_Active' (binary squeeze status)
            - 'Close' (current price)
            - Optional: 'bb_upper', 'bb_lower', 'kc_upper', 'kc_lower' for advanced filtering
        mode: 'active' or 'breakout' - which condition to check
            
    Returns:
        pd.DataFrame: Single-row DataFrame of the most recent data if condition met,
                     else empty DataFrame
    """
    if len(df) == 0 or 'TTM_squeeze_Active' not in df.columns:
        return pd.DataFrame()
    
    latest_row = df.iloc[-1]
    
    if mode == 'active':
        # Check if squeeze is currently active
        if latest_row['TTM_squeeze_Active'] == 1:
            return pd.DataFrame([latest_row])
            
    elif mode == 'breakout':
        # Check if squeeze just breakoutd (was active previous bar)
        if len(df) > 1:
            prev_row = df.iloc[-2]
            if prev_row['TTM_squeeze_Active'] == 1 and latest_row['TTM_squeeze_Active'] == 0:
                return pd.DataFrame([latest_row])
    
    return pd.DataFrame()  # Return empty if condition not met
