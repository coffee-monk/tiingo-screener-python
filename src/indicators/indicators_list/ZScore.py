import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators

def calculate_zscore_probability(df, 
                                 centreline="peaks_valleys_avg", 
                                 std_lookback=75, 
                                 avg_lookback=20, 
                                 **kwargs):
    """
    Calculate Z-Score based on price deviation from specified centreline
    
    Parameters:
    -----------
    df : pd.DataFrame
        Price data containing at least 'Close' column
    std_lookback : int
        Lookback period for standard deviation calculation (default: 75)
    centreline : str
        Type of centreline to use. Options:
        - "peaks_valleys_avg" : Average of peak/valley anchored VWAPs (default)
        - "gaps_avg" : Average of gap anchored VWAPs
        - "OB_avg" : Average of order block anchored VWAPs
        - "SMA" : Simple Moving Average
    avg_lookback : int
        Rolling window for average calculation (applies to all centreline types)
        Defaults:
        - 20 for peaks_valleys_avg
        - 1 for OB_avg
        - 10 for gaps_avg
    **kwargs : 
        Additional parameters for specific centreline types:
        - peaks_valleys_params : dict
        - gaps_params : dict
        - OB_params : dict
        - sma_periods : int
    """
    
    # Default lookbacks per centreline type
    default_lookbacks = {
        'peaks_valleys_avg': 20,
        'OB_avg': 1,
        'gaps_avg': 20
    }
    
    # Use provided avg_lookback or centreline-specific default
    final_lookback = (avg_lookback if avg_lookback is not None 
                     else default_lookbacks.get(centreline, None))

    # Centreline configurations
    centreline_config = {
        'peaks_valleys_avg': {
            'indicator': 'aVWAP',
            'params': {
                'peaks_valleys': False,
                'peaks_valleys_avg': True,
                'peaks_valleys_params': kwargs.get('peaks_valleys_params', 
                                                  {'periods': 20, 'max_aVWAPs': None}),
                'avg_lookback': final_lookback
            },
            'mean_col': 'Peaks_Valleys_avg'
        },
        'OB_avg': {
            'indicator': 'aVWAP',
            'params': {
                'OB': False,
                'OB_avg': True,
                'OB_params': kwargs.get('OB_params', 
                                      {'periods': 20, 'max_aVWAPs': None}),
                'avg_lookback': final_lookback
            },
            'mean_col': 'OB_avg'
        },
        'gaps_avg': {
            'indicator': 'aVWAP', 
            'params': {
                'gaps': False,
                'gaps_avg': True,
                'gaps_params': kwargs.get('gaps_params', 
                                         {'max_aVWAPs': 10}),
                'avg_lookback': final_lookback
            },
            'mean_col': 'Gaps_avg'
        },
        'SMA': {
            'indicator': 'SMA',
            'params': {'periods': [kwargs.get('sma_periods', 75)]},
            'mean_col': f"SMA_{kwargs.get('sma_periods', 75)}"
        }
    }

    # Validate and get config
    if centreline not in centreline_config:
        raise ValueError(f"Invalid centreline. Valid options: {list(centreline_config.keys())}")
    
    config = centreline_config[centreline]
    df = get_indicators(df, [config['indicator']], {config['indicator']: config['params']})
    
    # Calculate Z-Score
    mean_line = df[config['mean_col']]
    price_deviation = df['Close'] - mean_line
    z_score = price_deviation / price_deviation.rolling(std_lookback).std()

    return {'ZScore': z_score}

def calculate_indicator(df, **params):
    return calculate_zscore_probability(df, **params)
