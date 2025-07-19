import pandas as pd

def aVWAP_peaks_avg(df, distance_pct=1.0, direction='within'):
    """
    Scan for price near pre-calculated Peaks_avg level.
    Strictly uses existing Peaks_avg column without recalculation.
    
    Parameters:
        df: DataFrame with Peaks_avg column
        distance_pct: Percentage distance threshold
        direction: 'below', 'above', or 'within' relative to Peaks_avg
    
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty.
        Includes all original Peaks_avg parameters from input data.
    """
    # Validate input
    if len(df) == 0 or 'Peaks_avg' not in df.columns or 'Close' not in df.columns:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    if pd.isna(latest['Peaks_avg']):
        return pd.DataFrame()
    
    # Calculate percentage distance
    distance = (latest['Close'] - latest['Peaks_avg']) / latest['Peaks_avg'] * 100
    
    # Directional conditions
    if direction == 'below':
        condition = (-distance_pct <= distance <= 0)
    elif direction == 'above':
        condition = (0 <= distance <= distance_pct)
    else:  # 'within'
        condition = abs(distance) <= distance_pct
    
    if condition:
        return pd.DataFrame({
            'Close': latest['Close'],
            'Signal': f'NearPeaksAvg_{direction}',
            'Peaks_avg': latest['Peaks_avg'],
            'Distance_Pct': distance,
            'Position': 'below' if distance < 0 else 'above'
        }, index=[latest.name])
    
    return pd.DataFrame()
