import pandas as pd

def aVWAP_peaks_avg(df, distance_pct=1.0, direction='below'):
    """
    Scan for price near the Peaks_avg level with directional control.
    
    Parameters:
        df: DataFrame with Peaks_avg column
        distance_pct: Percentage distance threshold (absolute value)
        direction: Where to look relative to Peaks_avg:
                  'below' - Only prices below Peaks_avg
                  'above' - Only prices above Peaks_avg  
                  'both' - Either side (default behavior)
    
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    if pd.isna(latest['Peaks_avg']):
        return pd.DataFrame()
    
    peaks_avg = latest['Peaks_avg']
    distance = (latest['Close'] - peaks_avg) / peaks_avg * 100
    
    # Directional checks
    if direction == 'below':
        condition = (-distance_pct <= distance <= 0)  # Below Peaks_avg only
    elif direction == 'above':
        condition = (0 <= distance <= distance_pct)  # Above Peaks_avg only
    else:  # 'both'
        condition = abs(distance) <= distance_pct  # Either side
    
    if condition:
        result = pd.DataFrame({
            'Close': latest['Close'],
            'Signal': f'NearPeaksAvg_{direction}',
            'Peaks_avg': peaks_avg,
            'Distance_Pct': distance,
            'Position': 'below' if distance < 0 else 'above'
        }, index=[latest.name])
        return result
    
    return pd.DataFrame()
