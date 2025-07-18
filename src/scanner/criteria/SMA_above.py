import pandas as pd

def SMA_above(df, sma_periods=[50, 200], distance_pct=10.0, outside_range=False):
    """
    Detect when price is above moving averages, with option to scan outside distance threshold.
    
    Parameters:
        - df: DataFrame with price and SMA columns
        - sma_periods: List of SMA periods to check
        - distance_pct: Percentage distance threshold
        - outside_range: If True, finds prices ABOVE distance_pct (overbought)
        
    Returns:
        pd.DataFrame: Filtered results with Distance_Pct and Position
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    results = []
    
    for period in sma_periods:
        sma_col = f'SMA_{period}'
        
        if sma_col not in df.columns or pd.isna(latest[sma_col]):
            continue
            
        if latest['Close'] > latest[sma_col]:
            actual_distance = ((latest['Close'] - latest[sma_col]) / latest['Close']) * 100
            
            condition_met = (
                (not outside_range and (distance_pct is None or actual_distance <= distance_pct)) or
                (outside_range and distance_pct is not None and actual_distance > distance_pct)
            )
            
            if condition_met:
                result = latest.copy()
                result['SMA_Period'] = period
                result['Distance_Pct'] = actual_distance
                result['Position'] = 'Above' + (' (Extended)' if outside_range else '')
                results.append(result.to_frame().T)
    
    return pd.concat(results) if results else pd.DataFrame()
