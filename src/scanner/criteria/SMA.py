import pandas as pd

def SMA(df, sma_periods=[50, 200], distance_pct=1.0):
    """
    Scan for when price is near specified moving averages.
    
    Parameters:
        - df: DataFrame with price data and SMA columns
        - sma_periods: List of SMA periods to check (e.g., [50, 200])
        - distance_pct: Percentage distance from SMA to consider "close"
        
    Returns:
        pd.DataFrame: Single-row DataFrame if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    results = []
    
    for period in sma_periods:
        sma_col = f'SMA_{period}'
        
        if sma_col not in df.columns:
            continue  # Skip if this SMA isn't in the DataFrame
            
        if pd.isna(latest[sma_col]):
            continue  # Skip if SMA value is NaN
            
        # Calculate distance from current price to SMA
        distance = abs(latest['Close'] - latest[sma_col]) / latest['Close'] * 100
        
        if distance <= distance_pct:
            # Create a result entry
            result = latest.copy()
            result['SMA_Period'] = period
            result['Distance_Pct'] = distance
            results.append(result.to_frame().T)
    
    if results:
        return pd.concat(results)
    return pd.DataFrame()
