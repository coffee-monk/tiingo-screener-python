import pandas as pd
from smartmoneyconcepts import smc

def calculate_fvg(df, swing_length=25):

    df = df.rename(columns={
        'Open': 'open',
        'Close': 'close',
        'Low': 'low',
        'High': 'high',
        'Volume': 'volume'
    }).copy()

    swing_highs_lows = smc.swing_highs_lows(df, swing_length=swing_length)

    result = smc.ob(df, swing_highs_lows, close_mitigation=False)
    result.index = df.index # to preserve the datetime index
    
    df = pd.concat([df, result], axis=1)
    
    df = df.drop(columns=['Percentage', 'MitigatedIndex'], errors='ignore')
    df = df.rename(columns={'Top': 'OB_Top'}, errors='ignore')
    df = df.rename(columns={'Bottom': 'OB_Bottom'}, errors='ignore')
    df = df.rename(columns={'OBVolume': 'OB_Volume'}, errors='ignore')
    df = df.fillna(0)

    return {
        'OB': df['OB'],
        'OB_Top': df['OB_Top'],
        'OB_Bottom': df['OB_Bottom'] 
    }

def calculate_indicator(df, **params):
    """
    Wrapper function to calculate Fair Value Gaps (FVG).
    """
    return calculate_fvg(df, **params)
