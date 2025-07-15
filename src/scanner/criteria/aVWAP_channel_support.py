import pandas as pd

def aVWAP_channel_support(df, distance_pct=5.0, direction='within'):
    """
    Enhanced version with 'within' range check for 'within' direction.
    
    Parameters:
        df: DataFrame with aVWAP columns
        distance_pct: Percentage threshold
        direction: 
            'below' - Price must be ≥X% below aVWAP (distance <= -X%)
            'above' - Price must be ≥X% above aVWAP (distance >= X%)
            'within' - Price must be WITHIN X% of aVWAP (abs(distance) <= X%)
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    aVWAP_cols = [col for col in df.columns if col.startswith('aVWAP_')]
    current_aVWAPs = [latest[col] for col in aVWAP_cols if pd.notna(latest[col])]
    
    if not current_aVWAPs or pd.isna(latest['Close']):
        return pd.DataFrame()
    
    lowest_aVWAP = min(current_aVWAPs)
    distance = (latest['Close'] - lowest_aVWAP) / lowest_aVWAP * 100
    
    # Updated conditions
    if direction == 'below':
        condition = (distance <= -distance_pct)  # At least X% below
    elif direction == 'above':
        condition = (distance >= distance_pct)  # At least X% above
    else:  # 'within' (now checks for within range)
        condition = (abs(distance) <= distance_pct)  # Within X% range
    
    if condition:
        return pd.DataFrame({
            'Close': latest['Close'],
            'Signal': f'aVWAP_Support_{direction}',
            'Lowest_aVWAP': lowest_aVWAP,
            'Distance_Pct': distance,
            'Threshold_Pct': distance_pct,
            'Position': 'below' if distance < 0 else 'above'
        }, index=[latest.name])
    
    return pd.DataFrame()
