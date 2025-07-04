import pandas as pd

def aVWAP_avg_below(df, distance_pct=None):
    """
    Scan for when price is below the Peaks_Valleys average level.
    
    Parameters:
        - df: DataFrame with price data and Peaks_Valleys_avg column
        - distance_pct: Optional max percentage distance below Peaks_Valleys_avg to consider
        
    Returns:
        pd.DataFrame: Single-row DataFrame if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    if 'Peaks_Valleys_avg' not in df.columns or pd.isna(latest['Peaks_Valleys_avg']):
        return pd.DataFrame()
    
    if latest['Close'] < latest['Peaks_Valleys_avg']:
        distance = ((latest['Peaks_Valleys_avg'] - latest['Close']) / latest['Close'] * 100)
        
        if distance_pct is None or distance <= distance_pct:
            result = latest.copy()
            result['Distance_Pct'] = distance
            result['Position'] = 'Below'
            return result.to_frame().T
    
    return pd.DataFrame()
