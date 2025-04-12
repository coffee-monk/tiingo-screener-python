import importlib
import pandas as pd

def get_indicators(df, indicator_names, indicator_params=None):
    """
    Calculate and add indicators to the DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        indicator_names (list): List of indicator names to calculate.
        indicator_params (dict): Dictionary of parameters for each indicator.
                                 Format: {indicator_name: {param_name: param_value}}.
                                 Example: {'peaks_valleys': {'window_size': 50}}.

    Returns:
        pd.DataFrame: DataFrame with added indicator columns.
    """
    if indicator_params is None:
        indicator_params = {}

    for indicator_name in indicator_names:
        # Dynamically import the indicator module
        module = importlib.import_module(f"src.indicators.indicators_list.{indicator_name}")
        
        # Get parameters for the current indicator (if any)
        params = indicator_params.get(indicator_name, {})

        # Calculate the indicator values
        indicator_values = module.calculate_indicator(df, **params)
        
        # Append indicator values to DataFrame
        if isinstance(indicator_values, pd.DataFrame):
            df = pd.concat([df, indicator_values], axis=1)  # If indicator returns DataFrame, merge with main DataFrame
        elif isinstance(indicator_values, dict):
            for col_name, col_data in indicator_values.items():  # If indicator returns dictionary, add each key-value as column
                df[col_name] = col_data
        else:
            df[indicator_name] = indicator_values  # If indicator returns a single column, add directly
    
    return df
