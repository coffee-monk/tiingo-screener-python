import pandas as pd

def calculate_simple_moving_averages(df, periods=[200], **params):
    sma_dict = {}
    
    for period in periods:
        # Validate period size
        if not isinstance(period, int) or period <= 0:
            raise ValueError(f"period size must be positive integer, got {period}")
            
        # Calculate SMA and store in dictionary
        col_name = f'SMA_{period}'
        sma_dict[col_name] = df['Close'].rolling(window=period).mean()
    
    return sma_dict

def calculate_indicator(df, **params):
    return calculate_simple_moving_averages(df, **params)
