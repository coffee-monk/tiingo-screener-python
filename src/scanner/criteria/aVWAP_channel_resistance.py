import pandas as pd

def aVWAP_channel_resistance(df, distance_pct=1.0, direction='above'):
    """
    Scan for price near the highest aVWAP in the channel (resistance level).
    
    Parameters:
        df: DataFrame with aVWAP_peak_* and aVWAP_valley_* columns
        distance_pct: Percentage distance from resistance level 
                     (positive = above resistance, negative = below resistance)
        direction: Where to look relative to resistance:
                  'above' - Only prices above resistance (breakouts)
                  'below' - Only prices below resistance (rejections)
                  'both' - Either side (default behavior)
    
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    # Get all active aVWAP values
    aVWAP_cols = [col for col in df.columns if col.startswith('aVWAP_')]
    current_aVWAPs = [latest[col] for col in aVWAP_cols if pd.notna(latest[col])]
    
    # Need at least one valid aVWAP
    if not current_aVWAPs:
        return pd.DataFrame()
    
    # Calculate resistance level (highest aVWAP)
    resistance_level = max(current_aVWAPs)
    lowest_aVWAP = min(current_aVWAPs)
    
    # Calculate percentage distance from resistance
    distance = (latest['Close'] - resistance_level) / resistance_level * 100
    
    # Directional checks
    if direction == 'below':
        condition = (-distance_pct <= distance <= 0)  # Below resistance only
    elif direction == 'above':
        condition = (0 <= distance <= distance_pct)  # Above resistance only
    else:  # 'both'
        condition = abs(distance) <= distance_pct  # Either side
    
    if condition:
        result = pd.DataFrame({
            'Resistance_Level': resistance_level,
            'Support_Level': lowest_aVWAP,  # For context
            'Distance_Pct': distance,
            'Position': 'below' if distance < 0 else 'above',
            'Channel_Width_Pct': (resistance_level - lowest_aVWAP) / lowest_aVWAP * 100
        }, index=[latest.name])
        
        return result
    
    return pd.DataFrame()
