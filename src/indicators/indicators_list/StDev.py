import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators

def calculate_stdev_bands(df, 
                         centreline="peaks_valleys_avg", 
                         stdev_lookback=75, 
                         avg_lookback=20,
                         **kwargs):
    """
    Calculate standard deviation bands around dynamic centrelines
    
    Parameters:
    -----------
    df : pd.DataFrame
        Price data containing at least 'Close' column
    stdev_lookback : int
        Lookback period for standard deviation calculation (default: 20)
    centreline : str
        Type of centreline to use. Options:
        - "peaks_valleys_avg" : Average of peak/valley anchored VWAPs (default)
        - "gaps_avg" : Average of gap anchored VWAPs
        - "OB_avg" : Average of order block anchored VWAPs
        - "SMA" : Simple Moving Average
    avg_lookback : int
        Rolling window for average calculation (applies to all centreline types)
    **kwargs : 
        Additional parameters for specific centreline types:
        - peaks_valleys_params : dict
        - gaps_params : dict
        - OB_params : dict
        - sma_periods : int
    
    Returns:
    --------
    dict
        {
            'StDev': Standard deviation values,
            'UpperBand': Centreline + (StDev * num_std),
            'LowerBand': Centreline - (StDev * num_std),
            'Centreline': The mean line used
        }
    """
    
    # Default lookbacks per centreline type
    default_lookbacks = {
        'peaks_valleys_avg': 20,
        'OB_avg': 1,
        'gaps_avg': 20
    }
    
    final_lookback = (avg_lookback if avg_lookback is not None 
                     else default_lookbacks.get(centreline, None))

    # Centreline configurations (same structure as ZScore)
    centreline_config = {
        'peaks_valleys_avg': {
            'indicator': 'aVWAP',
            'params': {
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
                'gaps_avg': True,
                'gaps_params': kwargs.get('gaps_params', 
                                         {'max_aVWAPs': 10}),
                'avg_lookback': final_lookback
            },
            'mean_col': 'Gaps_avg'
        },
        'SMA': {
            'indicator': 'SMA',
            'params': {'periods': [kwargs.get('sma_periods', stdev_lookback)]},
            'mean_col': f"SMA_{kwargs.get('sma_periods', stdev_lookback)}"
        }
    }

    # Validate centreline
    if centreline not in centreline_config:
        raise ValueError(f"Invalid centreline. Valid options: {list(centreline_config.keys())}")
    
    config = centreline_config[centreline]
    df = get_indicators(df, [config['indicator']], {config['indicator']: config['params']})
    mean_line = df[config['mean_col']]

    # Calculate Bollinger-style metrics
    price_std = df['Close'].rolling(window=stdev_lookback).std()

    zscore = (df['Close'] - mean_line) / price_std
    
    return {
        'StDev': price_std,
        # 'UpperBand_1': mean_line + price_std,
        # 'LowerBand_1': mean_line - price_std,
        # 'UpperBand_2': mean_line + (2 * price_std),
        # 'LowerBand_2': mean_line - (2 * price_std),
        'StDev_Mean': mean_line,
        'StdDev_ZScore': zscore,
    }

def calculate_indicator(df, **params):
    """Standard interface for indicator calculation"""
    return calculate_stdev_bands(df, **params)
