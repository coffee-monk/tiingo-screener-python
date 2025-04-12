import pandas as pd
from smartmoneyconcepts import smc

def calculate_fvg(df):

    df = df.rename(columns={
        'Open': 'open',
        'Close': 'close',
        'Low': 'low',
        'High': 'high',
        'Volume': 'volume'
    }).copy()

    result = smc.fvg(df, join_consecutive=False)
    result.index = df.index

    df = pd.concat([df, result], axis=1)

    df = df.drop(columns=['Valleys', 'Peaks'], errors='ignore')
    df = df.rename(columns={'Top': 'FVG_Top'}, errors='ignore')
    df = df.rename(columns={'Bottom': 'FVG_Bottom'}, errors='ignore')
    df = df.rename(columns={'MitigatedIndex': 'FVG_Mitigated_Index'}, errors='ignore')
    df = df.fillna(0)

    return {
        'FVG': df['FVG'],
        'FVG_Top': df['FVG_Top'],
        'FVG_Bottom': df['FVG_Bottom'],
        'FVG_Mitigated_Index': df['FVG_Mitigated_Index'] 
    }

def calculate_indicator(df, **params):
    """
    Wrapper function to calculate Fair Value Gaps (FVG).
    """
    return calculate_fvg(df, **params)
