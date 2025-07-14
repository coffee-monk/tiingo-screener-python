import pandas as pd

def aVWAP_valleys_avg(df, distance_pct=1.0, direction='both'):
    """
    Scan for price near pre-calculated Valleys_avg level.
    Strictly uses existing Valleys_avg column without recalculation.
    
    Parameters:
        df: DataFrame with Valleys_avg column
        distance_pct: Percentage distance threshold
        direction: 'below', 'above', or 'both' relative to Valleys_avg
    
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty.
        Includes all original Valleys_avg parameters from input data.
    """
    # Validate input
    if len(df) == 0 or 'Valleys_avg' not in df.columns or 'Close' not in df.columns:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    if pd.isna(latest['Valleys_avg']):
        return pd.DataFrame()
    
    # Calculate percentage distance
    distance = (latest['Close'] - latest['Valleys_avg']) / latest['Valleys_avg'] * 100
    
    # Directional conditions
    if direction == 'below':
        condition = (-distance_pct <= distance <= 0)
    elif direction == 'above':
        condition = (0 <= distance <= distance_pct)
    else:  # 'both'
        condition = abs(distance) <= distance_pct
    
    if condition:
        return pd.DataFrame({
            'Close': latest['Close'],
            'Signal': f'NearValleysAvg_{direction}',
            'Valleys_avg': latest['Valleys_avg'],
            'Distance_Pct': distance,
            'Position': 'below' if distance < 0 else 'above'
        }, index=[latest.name])
    
    return pd.DataFrame()
