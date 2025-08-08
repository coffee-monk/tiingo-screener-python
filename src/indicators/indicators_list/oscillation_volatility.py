import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators

def calculate_oscillation_volatility(df,
                                   lookback=100,
                                   peaks_valleys_params={'periods': 20, 'max_aVWAPs': None},
                                   avg_lookback=20,
                                   include_ma_output=True,
                                   min_cross_std=0.2,  # Minimum std dev threshold for valid crosses
                                   **params):
    """
    Complete oscillation volatility indicator with:
    - Adjustable sensitivity via min_cross_std
    - Pure dictionary output
    - Standard deviation filtering
    """
    # 1. Calculate MA indicators
    try:
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
        ma = aVWAP_results['Peaks_Valleys_avg']
    except Exception as e:
        raise ValueError(f"MA calculation failed: {str(e)}")

    # 2. Initialize output series
    results = {
        'MA_Cross_Count': pd.Series(0, index=df.index),
        'MA_Avg_Deviation_Z': pd.Series(0.0, index=df.index),
        'MA_Oscillation_Score': pd.Series(0.0, index=df.index)
    }
    
    if include_ma_output:
        results['Peaks_Valleys_avg'] = ma

    price_std = df['Close'].rolling(lookback, min_periods=1).std().replace(0, np.nan)

    # 3. Calculate oscillations with sensitivity filter
    for i in range(lookback, len(df)):
        window_close = df['Close'].iloc[i-lookback:i].values
        window_ma = ma.iloc[i-lookback:i].values
        current_std = price_std.iloc[i]
        
        crosses = []
        deviations = []
        
        for j in range(1, len(window_close)):
            prev_close = window_close[j-1]
            prev_ma = window_ma[j-1]
            curr_close = window_close[j]
            curr_ma = window_ma[j]
            
            deviation = (curr_close - curr_ma) / current_std
            
            # Bullish cross with threshold check
            if (prev_close < prev_ma) and (curr_close > prev_ma):
                if abs(deviation) >= min_cross_std:
                    crosses.append(j)
                    deviations.append(abs(deviation))
            
            # Bearish cross with threshold check
            elif (prev_close > prev_ma) and (curr_close < prev_ma):
                if abs(deviation) >= min_cross_std:
                    crosses.append(j)
                    deviations.append(abs(deviation))

        if crosses and not np.isnan(current_std):
            avg_dev = np.mean(deviations)
            results['MA_Avg_Deviation_Z'].iloc[i] = avg_dev
            results['MA_Cross_Count'].iloc[i] = len(crosses)
            results['MA_Oscillation_Score'].iloc[i] = len(crosses) * avg_dev

    return results

def calculate_indicator(df, **params):
    return calculate_oscillation_volatility(df, **params)
