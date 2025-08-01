import pandas as pd
from typing import Literal, Optional

def aVWAP_avg(
    df: pd.DataFrame,
    mode: Literal['combined', 'peaks', 'valleys'] = 'combined',
    distance_pct: float = 1.0,
    direction: Literal['below', 'above', 'within'] = 'within',
    outside_range: bool = False
) -> pd.DataFrame:
    """
    Unified scanner for price relative to aVWAP averages (combined, peaks, or valleys).
    
    Parameters:
        df: DataFrame containing:
            - 'Close' (current price)
            - One of:
                - 'Peaks_Valleys_avg' (for mode='combined')
                - 'Peaks_avg' (for mode='peaks')
                - 'Valleys_avg' (for mode='valleys')
            
        mode: Which average to use:
            - 'combined': Uses 'Peaks_Valleys_avg' (both peaks and valleys)
            - 'peaks': Uses 'Peaks_avg' (only peaks)
            - 'valleys': Uses 'Valleys_avg' (only valleys)
            
        distance_pct: Percentage distance threshold from average
        direction: Price position relative to average:
            - 'below': Price below average
            - 'above': Price above average
            - 'within': Price near average (either side)
        outside_range: If True, finds prices BEYOND distance_pct threshold
                     (overbought/oversold), if False finds prices WITHIN threshold
    
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()

    # Determine which column to use based on mode
    if mode == 'combined':
        avg_col = 'Peaks_Valleys_avg'
        signal_prefix = 'aVWAP_avg'
    elif mode == 'peaks':
        avg_col = 'Peaks_avg'
        signal_prefix = 'Peaks_avg'
    elif mode == 'valleys':
        avg_col = 'Valleys_avg'
        signal_prefix = 'Valleys_avg'
    else:
        raise ValueError("mode must be 'combined', 'peaks', or 'valleys'")

    if avg_col not in df.columns:
        return pd.DataFrame()

    latest = df.iloc[-1]
    current_avg = latest[avg_col]

    if pd.isna(current_avg) or pd.isna(latest['Close']):
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
            position_desc = 'Below ' + ('aVWAP' if mode == 'combined' else mode) + (' (Extended)' if outside_range else '')
        elif direction == 'above':
            position_desc = 'Above ' + ('aVWAP' if mode == 'combined' else mode) + (' (Extended)' if outside_range else '')
        else:
            position_desc = 'Near ' + ('aVWAP' if mode == 'combined' else mode) + (' (Extended)' if outside_range else '')
        
        return pd.DataFrame({
            'Close': latest['Close'],
            'Signal': f'{signal_prefix}_{direction}' + ('_extended' if outside_range else ''),
            'Average_Level': current_avg,
            'Distance_Pct': distance,
            'Position': position_desc,
            'Mode': mode
        }, index=[latest.name])
    
    return pd.DataFrame()

def calculate_indicator(df, **params):
    """Standard interface wrapper"""
    return aVWAP_avg_scan(df, **params)
