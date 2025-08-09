import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators

def calculate_oscillation_volatility(
    df,
    lookback=100,
    peaks_valleys_params={'periods': 20, 'max_aVWAPs': None},
    avg_lookback=20,
    include_ma_output=True,
    min_cross_std=0.1,
    **params
):
    """
    Robust oscillation volatility indicator with:
    - Automatic handling of insufficient data
    - Fallback calculations when peaks/valleys can't be determined
    - Clean error handling without additional parameters
    """
    
    # Initialize default results
    results = {
        'MA_Cross_Count': pd.Series(0, index=df.index),
        'MA_Avg_Deviation_Z': pd.Series(np.nan, index=df.index),
        'MA_Oscillation_Score': pd.Series(np.nan, index=df.index)
    }
    
    # Early return if insufficient data
    if len(df) < 2:
        return results

    try:
        # Attempt to get MA with peaks/valleys
        aVWAP_results = get_indicators(
            df[['Open', 'High', 'Low', 'Close', 'Volume']].copy(),
            ['aVWAP'],
            {'aVWAP': {
                'peaks_valleys': True,
                'peaks_valleys_avg': True,
                'peaks_valleys_params': peaks_valleys_params,
                'avg_lookback': avg_lookback
            }}
        )
        
        # Use peaks/valleys avg if available, otherwise fallback to simple aVWAP
        if 'Peaks_Valleys_avg' in aVWAP_results and not aVWAP_results['Peaks_Valleys_avg'].isna().all():
            ma = aVWAP_results['Peaks_Valleys_avg']
        else:
            ma = aVWAP_results['aVWAP']
            
        if include_ma_output:
            results['Peaks_Valleys_avg'] = ma
            
    except Exception as e:
        # If MA calculation fails completely, return default results
        return results

    # Calculate price std with robust handling
    price_std = df['Close'].rolling(lookback, min_periods=1).std()
    price_std = price_std.replace(0, np.nan).ffill().bfill()
    
    if price_std.isna().all():
        return results  # Can't proceed without valid std

    # Calculate oscillations with safe indexing
    valid_range = range(max(lookback, 1), len(df))
    
    for i in valid_range:
        try:
            window_close = df['Close'].iloc[i-lookback:i]
            window_ma = ma.iloc[i-lookback:i]
            current_std = price_std.iloc[i]
            
            if np.isnan(current_std):
                continue
                
            # Vectorized cross detection
            prev_close = window_close.shift(1)
            prev_ma = window_ma.shift(1)
            crosses = (
                ((prev_close < prev_ma) & (window_close > prev_ma)) |
                ((prev_close > prev_ma) & (window_close < prev_ma))
            )
            deviations = np.abs((window_close - window_ma) / current_std)
            valid_crosses = crosses & (deviations >= min_cross_std)
            
            if valid_crosses.any():
                avg_dev = deviations[valid_crosses].mean()
                results['MA_Avg_Deviation_Z'].iloc[i] = avg_dev
                results['MA_Cross_Count'].iloc[i] = valid_crosses.sum()
                results['MA_Oscillation_Score'].iloc[i] = valid_crosses.sum() * avg_dev
                
        except Exception:
            continue  # Skip any problematic windows

    return results

def calculate_indicator(df, **params):
    return calculate_oscillation_volatility(df, **params)
