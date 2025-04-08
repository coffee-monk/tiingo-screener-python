import pandas as pd
from smartmoneyconcepts import smc

def calculate_BoS_CHoCH(df, swing_length=25):

    df = df.rename(columns={
        'Open': 'open',
        'Close': 'close',
        'Low': 'low',
        'High': 'high',
        'Volume': 'volume'
    }).copy()

    swing_highs_lows = smc.swing_highs_lows(df, swing_length=swing_length)

    result = smc.bos_choch(df, swing_highs_lows, close_break=True)
    result.index = df.index # to preserve the datetime index

    df = pd.concat([df, result], axis=1)

    df = df.rename(columns={'BOS': 'BoS'}, errors='ignore')
    df = df.rename(columns={'CHOCH': 'CHoCH'}, errors='ignore')
    df = df.rename(columns={'Level': 'BoS_CHoCH_Price'}, errors='ignore')
    df = df.rename(columns={'BrokenIndex': 'BoS_CHoCH_Break_Index'}, errors='ignore')
    df = df.fillna(0)

    return {
        'BoS': df['BoS'],
        'CHoCH': df['CHoCH'],
        'BoS_CHoCH_Price': df['BoS_CHoCH_Price'],
        'BoS_CHoCH_Break_Index': df['BoS_CHoCH_Break_Index'] 
    }

def calculate_indicator(df, **params):
    """
    Wrapper function to calculate: 
        - Break of Structure (BoS) 
        - Change of Character (CHoCH)
    """
    return calculate_BoS_CHoCH(df, **params)
