import pandas as pd

def aVWAP_avg_below(df, distance_pct=None, outside_range=False):
    """
    Detect when price is below aVWAP, with option to scan outside distance threshold.
    
    Parameters:
        - df: DataFrame with price and Peaks_Valleys_avg column
        - distance_pct: Percentage distance threshold
        - outside_range: If True, finds prices BELOW distance_pct (oversold)
        
    Returns:
        pd.DataFrame: Filtered results with Distance_Pct and Position
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    if 'Peaks_Valleys_avg' not in df.columns or pd.isna(latest['Peaks_Valleys_avg']):
        return pd.DataFrame()
    
    if latest['Close'] < latest['Peaks_Valleys_avg']:
        actual_distance = ((latest['Peaks_Valleys_avg'] - latest['Close']) / latest['Close']) * 100
        
        condition_met = (
            (not outside_range and (distance_pct is None or actual_distance <= distance_pct)) or
            (outside_range and distance_pct is not None and actual_distance > distance_pct)
        )
        
        if condition_met:
            result = latest.copy()
            result['Distance_Pct'] = actual_distance
            result['Position'] = 'Below aVWAP' + (' (Extended)' if outside_range else '')
            return result.to_frame().T
    
    return pd.DataFrame()
