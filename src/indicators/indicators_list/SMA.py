import pandas as pd

def calculate_simple_moving_averages(df, sma_lengths=[50, 200], **params):
    sma_dict = {}
    
    for length in sma_lengths:
        # Validate length size
        if not isinstance(length, int) or length <= 0:
            raise ValueError(f"length size must be positive integer, got {length}")
            
        # Calculate SMA and store in dictionary
        col_name = f'SMA_{length}'
        sma_dict[col_name] = df['Close'].rolling(window=length).mean()
    
    return sma_dict

def calculate_indicator(df, **params):
    return calculate_simple_moving_averages(df, **params)
