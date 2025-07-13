import pandas as pd

def aVWAP_channel_support(df, distance_pct=1.0, direction='below'):
    """
    Scan for price near the lowest aVWAP with directional control.
    
    Parameters:
        df: DataFrame with aVWAP_peak_* and aVWAP_valley_* columns
        distance_pct: Percentage distance threshold (absolute value)
        direction: Where to look relative to support:
                  'below' - Only prices below lowest aVWAP
                  'above' - Only prices above lowest aVWAP  
                  'both' - Either side (default behavior)
    
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    aVWAP_cols = [col for col in df.columns if col.startswith('aVWAP_')]
    current_aVWAPs = [latest[col] for col in aVWAP_cols if pd.notna(latest[col])]
    
    if not current_aVWAPs:
        return pd.DataFrame()
    
    lowest_aVWAP = min(current_aVWAPs)
    distance = (latest['Close'] - lowest_aVWAP) / lowest_aVWAP * 100
    
    # Directional checks
    if direction == 'below':
        condition = (-distance_pct <= distance <= 0)  # Below support only
    elif direction == 'above':
        condition = (0 <= distance <= distance_pct)  # Above support only
    else:  # 'both'
        condition = abs(distance) <= distance_pct  # Either side
    
    if condition:
        result = pd.DataFrame({
            'Close': latest['Close'],
            'Signal': f'NearChannelSupport_{direction}',
            'Lowest_aVWAP': lowest_aVWAP,
            'Distance_Pct': distance,
            'Position': 'below' if distance < 0 else 'above'
        }, index=[latest.name])
        return result
    
    return pd.DataFrame()
