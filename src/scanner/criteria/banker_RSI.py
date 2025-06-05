import pandas as pd

def banker_RSI(df, threshold=15):
    """
    banker RSI (Loken) is active, ie has value greater than 0
    params:
        - threshold: threshold values with active range between 0-20
    """
    latest = df.iloc[-1] # last row
    if latest['banker_RSI'] > threshold:
        return df.iloc[-1:].copy() # Return as 1-row dataframe
    return pd.DataFrame()
