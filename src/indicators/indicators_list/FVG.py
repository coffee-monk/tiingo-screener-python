import pandas as pd
from smartmoneyconcepts import smc

def calculate_fvg(df, max_mitigated=10, max_unmitigated=10, join_consecutive=False):
    df = df.rename(columns={
        'Open': 'open',
        'Close': 'close',
        'Low': 'low',
        'High': 'high',
        'Volume': 'volume'
    }).copy()

    result = smc.fvg(df, join_consecutive=join_consecutive)
    result.index = df.index

    df = pd.concat([df, result], axis=1)

    df = df.drop(columns=['Valleys', 'Peaks'], errors='ignore')
    df = df.rename(columns={'Top': 'FVG_High'}, errors='ignore')
    df = df.rename(columns={'Bottom': 'FVG_Low'}, errors='ignore')
    df = df.rename(columns={'MitigatedIndex': 'FVG_Mitigated_Index'}, errors='ignore')
    df = df.fillna(0)
    
    # Get all FVG indices sorted by date (newest first)
    fvg_indices = df[df['FVG'] != 0].index[::-1]
    
    # Separate into mitigated and unmitigated
    mitigated = []
    unmitigated = []
    
    for idx in fvg_indices:
        mit_idx = int(df.loc[idx, 'FVG_Mitigated_Index'])
        if 0 < mit_idx < len(df):
            mitigated.append(idx)
        else:
            unmitigated.append(idx)
    
    # Take limited number of most recent mitigated and unmitigated
    show_indices = mitigated[:max_mitigated] + unmitigated[:max_unmitigated]
    
    # Create mask to keep only the selected FVGs
    mask = df.index.isin(show_indices)
    
    # Zero out FVGs that we don't want to show
    df.loc[~mask, 'FVG'] = 0
    df.loc[~mask, 'FVG_High'] = 0
    df.loc[~mask, 'FVG_Low'] = 0
    df.loc[~mask, 'FVG_Mitigated_Index'] = 0

    return {
        'FVG': df['FVG'],
        'FVG_High': df['FVG_High'],
        'FVG_Low': df['FVG_Low'],
        'FVG_Mitigated_Index': df['FVG_Mitigated_Index'] 
    }

def calculate_indicator(df, **params):
    return calculate_fvg(df, **params)
