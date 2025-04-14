import importlib
import pandas as pd

def get_indicators(df, indicator_names, indicator_params=None):
    """
    Calculate and add indicators to the DataFrame without fragmentation.
    """
    if indicator_params is None:
        indicator_params = {}

    # Create a clean copy to work with
    result_df = df.copy()
    
    # Collect all indicator data first
    all_indicators = {}
    
    for indicator_name in indicator_names:
        module = importlib.import_module(f"src.indicators.indicators_list.{indicator_name}")
        params = indicator_params.get(indicator_name, {})
        indicator_values = module.calculate_indicator(result_df, **params)
        
        if isinstance(indicator_values, pd.DataFrame):
            # Merge DataFrames in one operation
            result_df = pd.concat([result_df, indicator_values], axis=1).copy()
        elif isinstance(indicator_values, dict):
            # Collect dictionary items for bulk addition
            all_indicators.update(indicator_values)
        else:
            all_indicators[indicator_name] = indicator_values
    
    # Add all collected indicators at once
    if all_indicators:
        indicators_df = pd.DataFrame(all_indicators)
        result_df = pd.concat([result_df, indicators_df], axis=1).copy()
    
    return result_df
