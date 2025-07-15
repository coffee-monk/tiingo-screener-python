import pandas as pd

def aVWAP_channel_resistance(df, distance_pct=10.0, direction='above'):
    """
    Enhanced resistance scanner with 'within' range check for 'within' direction.
    
    Parameters:
        df: DataFrame with aVWAP columns
        distance_pct: Percentage threshold
        direction: 
            'above' - Price must be ≥X% above resistance (distance >= X%)
            'below' - Price must be ≥X% below resistance (distance <= -X%)
            'within' - Price must be WITHIN X% of resistance (abs(distance) <= X%)
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    aVWAP_cols = [col for col in df.columns if col.startswith('aVWAP_')]
    current_aVWAPs = [latest[col] for col in aVWAP_cols if pd.notna(latest[col])]
    
    if not current_aVWAPs or pd.isna(latest['Close']):
        return pd.DataFrame()
    
    highest_aVWAP = max(current_aVWAPs)
    distance = (latest['Close'] - highest_aVWAP) / highest_aVWAP * 100
    
    # Updated conditions
    if direction == 'above':
        condition = (distance >= distance_pct)  # At least X% above resistance
    elif direction == 'below':
        condition = (distance <= -distance_pct)  # At least X% below resistance
    else:  # 'within' (now checks for within range)
        condition = (abs(distance) <= distance_pct)  # Within X% range
    
    if condition:
        return pd.DataFrame({
            'Close': latest['Close'],
            'Signal': f'aVWAP_Resistance_{direction}',
            'Highest_aVWAP': highest_aVWAP,
            'Distance_Pct': distance,
            'Threshold_Pct': distance_pct,
            'Position': 'above' if distance > 0 else 'below',
            'Lowest_aVWAP': min(current_aVWAPs)  # Still included for context
        }, index=[latest.name])
    
    return pd.DataFrame()
