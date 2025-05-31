import pandas as pd

def banker_RSI(df):
    """banker RSI (Loken) is active, ie has value greater than 0"""
    latest = df.iloc[-1] # last row
    if latest['banker_RSI'] > 0:
        return df.iloc[-1:].copy() # Return as 1-row dataframe
    return pd.DataFrame()
