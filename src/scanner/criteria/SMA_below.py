import pandas as pd

def SMA_below(df, sma_periods=[50, 200], distance_pct=None):
    """
    Detect when price is below moving averages, optionally within max distance.
    
    Parameters:
        - df: DataFrame with price and SMA columns
        - sma_periods: List of SMA periods to check
        - distance_pct: Optional max % distance below SMA to consider
        
    Returns:
        pd.DataFrame: Results where Close < SMA (optionally within distance)
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    results = []
    
    for period in sma_periods:
        sma_col = f'SMA_{period}'
        
        if sma_col not in df.columns or pd.isna(latest[sma_col]):
            continue
            
        if latest['Close'] < latest[sma_col]:
            distance_pct = ((latest[sma_col] - latest['Close']) / latest['Close']) * 100
            
            if distance_pct is None or distance_pct <= distance_pct:
                result = latest.copy()
                result['SMA_Period'] = period
                result['Distance_Pct'] = distance_pct
                result['Position'] = 'Below'
                results.append(result.to_frame().T)
    
    return pd.concat(results) if results else pd.DataFrame()
