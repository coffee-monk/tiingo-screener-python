import pandas as pd

def aVWAP_avg(df, distance_pct=1.0, direction='within', outside_range=False):
    """
    Enhanced unified scanner for price relative to Peaks_Valleys_avg.
    
    Parameters:
        df: DataFrame with 'Peaks_Valleys_avg' and 'Close' columns
        distance_pct: Percentage distance threshold
        direction: Relationship to aVWAP:
                  'below' - Price relative to below aVWAP
                  'above' - Price relative to above aVWAP  
                  'within' - Price relative to either side of aVWAP
        outside_range: If True, finds prices BEYOND distance_pct threshold
                     (overbought/oversold), if False finds prices WITHIN threshold
    
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty.
    """
    if len(df) == 0 or 'Peaks_Valleys_avg' not in df.columns:
        return pd.DataFrame()

    latest = df.iloc[-1]
    current_avg = latest['Peaks_Valleys_avg']

    if pd.isna(current_avg):
        return pd.DataFrame()

    # Calculate percentage distance
    distance = (latest['Close'] - current_avg) / current_avg * 100

    # Directional conditions with outside_range support
    if direction == 'below':
        if outside_range:
            condition = (distance < -distance_pct)  # Extended below
        else:
            condition = (-distance_pct <= distance <= 0)  # Normal below
    elif direction == 'above':
        if outside_range:
            condition = (distance > distance_pct)  # Extended above
        else:
            condition = (0 <= distance <= distance_pct)  # Normal above
    else:  # 'within'
        if outside_range:
            condition = (abs(distance) > distance_pct)  # Extended either side
        else:
            condition = (abs(distance) <= distance_pct)  # Normal near

    if condition:
        position_desc = ''
        if direction == 'below':
            position_desc = 'Below aVWAP' + (' (Extended)' if outside_range else '')
        elif direction == 'above':
            position_desc = 'Above aVWAP' + (' (Extended)' if outside_range else '')
        else:
            position_desc = 'Near aVWAP' + (' (Extended)' if outside_range else '')
        
        return pd.DataFrame({
            'Close': latest['Close'],
            'Signal': f'aVWAP_avg_{direction}' + ('_extended' if outside_range else ''),
            'Peaks_Valleys_avg': current_avg,
            'Distance_Pct': distance,
            'Position': position_desc
        }, index=[latest.name])
    
    return pd.DataFrame()
