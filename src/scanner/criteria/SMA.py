import pandas as pd

def SMA(
        df, 
        sma_periods=[50, 200], 
        distance_pct=1.0, 
        mode='within', 
        outside_range=False
       ):
    """
    Combined SMA scanner that can detect:
    - Price within SMAs
    - Price above/below SMAs
    - Extended moves beyond SMAs
    
    Parameters:
        df (pd.DataFrame): DataFrame with price data and SMA columns
        sma_periods (list): List of SMA periods to check (e.g., [50, 200])
        mode (str): One of ['within', 'above', 'below'] - determines scan type
        distance_pct (float): Percentage distance threshold
        outside_range (bool): 
            - For 'within' mode: N/A
            - For 'above'/'below' modes: 
                False = within distance_pct (normal)
                True = beyond distance_pct (extended move)
    
    Returns:
        pd.DataFrame: Results with Distance_Pct and Position columns
    """
    
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    results = []
    
    for period in sma_periods:
        sma_col = f'SMA_{period}'
        
        # Skip if SMA column doesn't exist or is NaN
        if sma_col not in df.columns or pd.isna(latest[sma_col]):
            continue
            
        current_price = latest['Close']
        sma_value = latest[sma_col]
        
        # Calculate distance percentage (always positive)
        distance = abs(current_price - sma_value) / current_price * 100
        
        # Determine position relative to SMA
        position = 'Above' if current_price > sma_value else 'Below'
        
        # Check conditions based on scan mode
        condition_met = False
        
        if mode == 'within':
            condition_met = (distance <= distance_pct)
            position = 'Within'
            
        elif mode == 'above':
            if current_price > sma_value:
                if outside_range:
                    condition_met = (distance > distance_pct)
                    position += ' (Extended)'
                else:
                    condition_met = (distance <= distance_pct)
                    
        elif mode == 'below':
            if current_price < sma_value:
                if outside_range:
                    condition_met = (distance > distance_pct)
                    position += ' (Extended)'
                else:
                    condition_met = (distance <= distance_pct)
        
        if condition_met:
            result = latest.copy()
            result['SMA_Period'] = period
            result['Distance_Pct'] = distance
            result['Position'] = position
            results.append(result.to_frame().T)
    
    return pd.concat(results) if results else pd.DataFrame()
