import pandas as pd
from smartmoneyconcepts import smc

def calculate_ob(df, periods=25):

    df = df.rename(columns={
        'Open': 'open',
        'Close': 'close',
        'Low': 'low',
        'High': 'high',
        'Volume': 'volume'
    }).copy()

    swing_highs_lows = smc.swing_highs_lows(df, swing_length=periods)

    result = smc.ob(df, swing_highs_lows, close_mitigation=False)
    result.index = df.index # to preserve the datetime index
    
    df = pd.concat([df, result], axis=1)
    
    df = df.drop(columns=['Percentage'], errors='ignore')
    df = df.rename(columns={'Top': 'OB_High'}, errors='ignore')
    df = df.rename(columns={'Bottom': 'OB_Low'}, errors='ignore')
    df = df.rename(columns={'OBVolume': 'OB_Volume'}, errors='ignore')
    df = df.rename(columns={'MitigatedIndex': 'OB_Mitigated_Index'}, errors='ignore')
    df = df.fillna(0)

    return {
        'OB': df['OB'],
        'OB_High': df['OB_High'],
        'OB_Low': df['OB_Low'],
        'OB_Mitigated_Index': df['OB_Mitigated_Index'] 
    }

def calculate_indicator(df, **params):
    return calculate_ob(df, **params)
