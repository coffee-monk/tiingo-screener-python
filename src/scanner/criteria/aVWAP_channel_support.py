import pandas as pd

def aVWAP_channel_support(df, distance_pct=10.0, direction='below'):
    """
    Scan for price MINIMUM distance from lowest aVWAP.
    
    Parameters:
        df: DataFrame with aVWAP_peak_* and aVWAP_valley_* columns
        distance_pct: MINIMUM percentage distance required
        direction: Where to look relative to support:
                  'below' - Price must be AT LEAST distance_pct% below lowest aVWAP
                  'above' - Price must be AT LEAST distance_pct% above lowest aVWAP  
                  'both' - Price must be AT LEAST distance_pct% away (either side)
    
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty.
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
    
    # New MINIMUM distance checks
    if direction == 'below':
        condition = (distance <= -distance_pct)  # Must be at least X% below
    elif direction == 'above':
        condition = (distance >= distance_pct)  # Must be at least X% above
    else:  # 'both'
        condition = (abs(distance) >= distance_pct)  # Must be at least X% away
    
    if condition:
        result = pd.DataFrame({
            'Close': latest['Close'],
            'Signal': f'MinChannelDistance_{direction}',
            'Lowest_aVWAP': lowest_aVWAP,
            'Distance_Pct': distance,
            'Min_Required_Pct': distance_pct,
            'Position': 'below' if distance < 0 else 'above'
        }, index=[latest.name])
        return result
    
    return pd.DataFrame()
