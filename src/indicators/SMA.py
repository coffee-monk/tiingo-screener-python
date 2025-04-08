import pandas as pd

def calculate_simple_moving_averages(df, sma_lengths=[50, 200], **params):
    """
    Calculate multiple simple moving averages based on user-provided length sizes.

    Parameters:
        df (pd.DataFrame): The input DataFrame
        sma_lengths (list): List of integers representing length sizes
        **params: Additional parameters (unused in this function)

    Returns:
        dict: Dictionary with SMA columns (keys: 'SMA_{length}')
    """
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
    """
    Wrapper function to calculate moving averages.

    Parameters:
        df (pd.DataFrame): The input DataFrame
        **params: Parameters to pass to calculate_simple_moving_averages()
                  Must include 'sma_lengths' parameter

    Returns:
        dict: Dictionary with SMA columns
    """
    return calculate_simple_moving_averages(df, **params)


# Example usage:
if __name__ == "__main__":
    # Create sample data
    data = {'Close': [i for i in range(1, 101)]}  # 1 to 100
    df = pd.DataFrame(data)
    
    # Calculate with default lengths
    default_result = calculate_indicator(df)
    print("Default lengths (20,50,200):")
    print(list(default_result.keys()))
    
    # Calculate with custom lengths
    custom_result = calculate_indicator(df, sma_lengths=[5, 10, 15, 30])
    print("\nCustom lengths (5,10,15,30):")
    print(list(custom_result.keys()))
