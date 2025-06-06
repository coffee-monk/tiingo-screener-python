import pandas as pd

def QQEMOD_oversold(df):
    """
    Scans for the 'red' condition in QQEMOD (strong bearish signal).
    
    Conditions:
    1. QQE1 below lower Bollinger Band (oversold in downtrend).
    2. QQE2 below its negative threshold (momentum confirms).
    3. QQE2 below its trendline (no reversal yet).
    
    Returns:
        pd.DataFrame: Latest row if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    red_conditions = (
        latest['QQE1_Below_Lower'] and
        latest['QQE2_Below_Threshold'] and
        not latest['QQE2_Above_TL']
    )
    
    if red_conditions:
        return pd.DataFrame([latest])  # Return the latest row
    return pd.DataFrame()  # Empty if no match
