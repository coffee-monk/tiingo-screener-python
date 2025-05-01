import pandas as pd
from smartmoneyconcepts import smc

def calculate_liquidity(df, swing_length=25, range_percent=0.1):

    df = df.rename(columns={
        'Open': 'open',
        'Close': 'close',
        'Low': 'low',
        'High': 'high',
        'Volume': 'volume'
    }).copy()

    swing_highs_lows = smc.swing_highs_lows(df, swing_length=swing_length)

    result = smc.liquidity(df, swing_highs_lows, range_percent=0.2)
    result.index = df.index # to preserve the datetime index
    
    df = pd.concat([df, result], axis=1)
    df = df.drop(columns=['End', 'Swept'], errors='ignore')
    df = df.rename(columns={'Level': 'Liquidity_Level'}, errors='ignore')
    df = df.fillna(0)

    return {
        'Liquidity': df['Liquidity'],
        'Liquidity_Level': df['Liquidity_Level'],
    }

def calculate_indicator(df, **params):
    return calculate_liquidity(df, **params)
