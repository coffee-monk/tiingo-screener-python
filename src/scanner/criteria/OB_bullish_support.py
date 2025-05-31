import pandas as pd
 
def OB_bullish_support(df):
    """
    Returns: 
        pd.DataFrame: Single-row DataFrame of the most recent bullish OB if price is in range,
                     else empty DataFrame
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    current_price = df['Close'].iloc[-1]
    
    # Search backward for most recent bullish OB
    for i in range(len(df)-1, -1, -1):
        if df['OB'].iloc[i] == 1:
            ob = df.iloc[i]
            # check that current price is within the OB
            if ob['OB_Low'] <= current_price <= ob['OB_High']:
                return pd.DataFrame([ob])  # Return as single-row DataFrame
            break
    
    return pd.DataFrame()  # Return empty DataFrame if no match
