import pandas as pd

def aVWAP_avg(df, distance_pct=1.0):
    """
    Scan for when price is near the Peaks_Valleys average level.
    
    Parameters:
        - df: DataFrame with price data and Peaks_Valleys_avg column
        - distance_pct: Percentage distance from Peaks_Valleys_avg to consider "close"
        
    Returns:
        pd.DataFrame: Single-row DataFrame if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    # Check if Peaks_Valleys_avg exists and has a valid value
    if 'Peaks_Valleys_avg' not in df.columns or pd.isna(latest['Peaks_Valleys_avg']):
        return pd.DataFrame()
    
    # Calculate distance from current price to Peaks_Valleys_avg
    distance = abs(latest['Close'] - latest['Peaks_Valleys_avg']) / latest['Close'] * 100
    
    if distance <= distance_pct:
        # Create a result entry
        result = latest.copy()
        result['Distance_Pct'] = distance
        return result.to_frame().T
    
    return pd.DataFrame()
