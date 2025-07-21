import pandas as pd
from typing import Literal, Optional

def aVWAP_channel(
    df: pd.DataFrame,
    mode: Literal['support', 'resistance'] = 'support',
    distance_pct: float = 5.0,
    direction: Literal['below', 'above', 'within'] = 'within',
    include_extremes: bool = False
) -> pd.DataFrame:
    """
    Unified aVWAP channel scanner for support/resistance levels.
    
    Parameters:
        df: DataFrame containing:
            - Columns starting with 'aVWAP_'
            - 'Close' (current price)
            
        mode: 'support' or 'resistance' - which level to scan for
            - support = bottom-most peaks aVWAP of the channel
            - resistance = top-most valleys aVWAP of the channel
        distance_pct: Percentage threshold from aVWAP level
        direction: Price position relative to aVWAP:
            - 'below': Price must be ≥X% below level
            - 'above': Price must be ≥X% above level  
            - 'within': Price must be within X% of level
        include_extremes: If True, includes both highest/lowest aVWAP in results
        
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    aVWAP_cols = [col for col in df.columns if col.startswith('aVWAP_') and pd.notna(latest[col])]
    
    if not aVWAP_cols or pd.isna(latest['Close']):
        return pd.DataFrame()
    
    # Get relevant aVWAP level
    if mode == 'support':
        target_aVWAP = min(latest[col] for col in aVWAP_cols)
        signal_prefix = 'aVWAP_Support'
    else:  # resistance
        target_aVWAP = max(latest[col] for col in aVWAP_cols)
        signal_prefix = 'aVWAP_Resistance'
    
    distance = (latest['Close'] - target_aVWAP) / target_aVWAP * 100
    
    # Check conditions
    if direction == 'below':
        condition = (distance <= -distance_pct)
    elif direction == 'above':
        condition = (distance >= distance_pct)
    else:  # 'within'
        condition = (abs(distance) <= distance_pct)
    
    if condition:
        result = {
            'Close': latest['Close'],
            'Signal': f'{signal_prefix}_{direction}',
            'aVWAP_Level': target_aVWAP,
            'Distance_Pct': distance,
            'Threshold_Pct': distance_pct,
            'Position': 'below' if distance < 0 else 'above'
        }
        
        if include_extremes:
            result.update({
                'Highest_aVWAP': max(latest[col] for col in aVWAP_cols),
                'Lowest_aVWAP': min(latest[col] for col in aVWAP_cols)
            })
        
        return pd.DataFrame(result, index=[latest.name])
    
    return pd.DataFrame()

def calculate_indicator(df, **params):
    """Standard interface wrapper"""
    return aVWAP_channel(df, **params)
