import pandas as pd

def aVWAP_valleys_avg(df, distance_pct=1.0, direction='below'):
    """
    Scan for price near the Valleys_avg level with directional control.
    
    Parameters:
        df: DataFrame with Valleys_avg column
        distance_pct: Percentage distance threshold (absolute value)
        direction: Where to look relative to Valleys_avg:
                  'below' - Only prices below Valleys_avg
                  'above' - Only prices above Valleys_avg  
                  'both' - Either side (default behavior)
    
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    if pd.isna(latest['Valleys_avg']):
        return pd.DataFrame()
    
    valleys_avg = latest['Valleys_avg']
    distance = (latest['Close'] - valleys_avg) / valleys_avg * 100
    
    # Directional checks
    if direction == 'below':
        condition = (-distance_pct <= distance <= 0)  # Below Valleys_avg only
    elif direction == 'above':
        condition = (0 <= distance <= distance_pct)  # Above Valleys_avg only
    else:  # 'both'
        condition = abs(distance) <= distance_pct  # Either side
    
    if condition:
        result = pd.DataFrame({
            'Close': latest['Close'],
            'Signal': f'NearValleysAvg_{direction}',
            'Valleys_avg': valleys_avg,
            'Distance_Pct': distance,
            'Position': 'below' if distance < 0 else 'above'
        }, index=[latest.name])
        return result
    
    return pd.DataFrame()
