import pandas as pd

def OB_bullish_below_aVWAP(df):
    """
    Finds when price is within/above a bullish Order Block but below its aVWAP.
    
    Parameters:
        df (pd.DataFrame): Must contain:
            - 'OB' (1=bullish, -1=bearish, 0=neutral)
            - 'OB_High', 'OB_Low' (price range of OB)
            - 'Close' (current price)
            - Columns matching 'aVWAP_OB_bull_*' pattern
            
    Returns:
        pd.DataFrame: Single-row DataFrame of current candle if conditions met,
                     else empty DataFrame
    """
    latest = df.iloc[-1]  # Last row (current candle)
    
    # Find most recent bullish OB (search backward)
    for i in range(len(df)-1, -1, -1):
        if df['OB'].iloc[i] == 1:
            ob_high = df['OB_High'].iloc[i]
            ob_low = df['OB_Low'].iloc[i]
            
            # Find corresponding aVWAP (format: aVWAP_OB_bull_[index])
            avwap_col = f'aVWAP_OB_bull_{i}'
            if avwap_col in df.columns:
                current_avwap = df[avwap_col].iloc[-1]
                
                # Check conditions:
                # 1. Price is within or above OB range (latest['Close'] >= ob_low)
                # 2. Price is below OB's aVWAP (latest['Close'] < current_avwap)
                if (latest['Close'] >= ob_low) and (latest['Close'] < current_avwap):
                    return df.iloc[-1:].copy()  # Return current candle as 1-row dataframe
            
            break  # Only check most recent OB
    
    return pd.DataFrame()  # Return empty if no match
