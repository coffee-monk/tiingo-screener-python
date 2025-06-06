import pandas as pd

def QQEMOD_overbought(df):
    """
    Scans for the 'teal' condition in QQEMOD (strong bullish signal).
    
    Conditions:
    1. QQE1 above upper Bollinger Band (overbought in uptrend).
    2. QQE2 above its positive threshold (momentum confirms).
    3. QQE2 above its trendline (no reversal yet).
    
    Returns:
        pd.DataFrame: Latest row if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    teal_conditions = (
        latest['QQE1_Above_Upper'] and
        latest['QQE2_Above_Threshold'] and
        latest['QQE2_Above_TL']
    )
    
    if teal_conditions:
        return pd.DataFrame([latest])  # Return the latest row
    return pd.DataFrame()  # Empty if no match
