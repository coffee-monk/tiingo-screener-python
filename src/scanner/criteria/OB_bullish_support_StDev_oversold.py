import pandas as pd

def OB_bullish_support_StDev_oversold(df, zscore_threshold=-1.0):
    """
    Checks if:
    1. Most recent OB is bullish (OB=1)
    2. Current price is inside this OB's range (OB_High to OB_Low)
    3. Current pre-calculated StdDev_ZScore < threshold (oversold)
    
    Parameters:
        df (pd.DataFrame): Must contain pre-calculated:
            - 'OB' (1=Bullish, -1=Bearish, 0=None)
            - 'OB_High', 'OB_Low' (price range)
            - 'Close' (current price)
            - 'StdDev_ZScore' (pre-calculated with chosen centerline)
        zscore_threshold (float): Oversold threshold (default: -1.0)
            
    Returns:
        pd.DataFrame: The qualifying bullish OB if all conditions met,
                     else empty DataFrame
    """
    if df.empty:
        return pd.DataFrame()
    
    # Find most recent OB (last non-zero OB in actual time)
    reversed_df = df.iloc[::-1]
    recent_OB = reversed_df[reversed_df['OB'] != 0].head(1)
    
    # Reject if no OB exists or if most recent is bearish
    if recent_OB.empty or recent_OB.iloc[0]['OB'] != 1:
        return pd.DataFrame()
    
    # Get current values from most recent candle
    current_close = df.iloc[-1]['Close']
    current_zscore = df.iloc[-1]['StdDev_ZScore']
    
    # Check price is inside OB range
    ob_high = recent_OB['OB_High'].values[0]
    ob_low = recent_OB['OB_Low'].values[0]
    price_inside = (current_close <= ob_high) and (current_close >= ob_low)
    
    # Check ZScore condition
    zscore_valid = current_zscore < zscore_threshold
    
    # Return OB if all conditions met
    if price_inside and zscore_valid:
        return recent_OB
    return pd.DataFrame()
