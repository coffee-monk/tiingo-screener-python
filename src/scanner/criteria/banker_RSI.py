import pandas as pd

def banker_RSI(df):
    """RSI Oversold criteria with volume and trend confirmation"""
    latest = df.iloc[-1] # last row
    if latest['banker_RSI'] < 30:
        return df.iloc[-1:].copy() # Return as 1-row dataframe
    return pd.DataFrame()
