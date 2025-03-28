import pandas as pd

def calculate_peaks_valleys(df, window_size=25, **params):
    """
    Calculate peaks and valleys based on rolling window.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        window_size (int): Size of the rolling window.
        **params: Additional parameters (unused in this function).

    Returns:
        dict: Dictionary with 'Valleys' and 'Peaks' columns.
    """
    valleys = df['Low'].rolling(window_size, center=True).min() / df['Low']
    peaks = df['High'].rolling(window_size, center=True).max() / df['High']

    # Peaks/valleys = 1.0, else = 0.0
    valleys = valleys.apply(lambda x: 1.0 if x == 1.0 else 0.0)
    peaks = peaks.apply(lambda x: 1.0 if x == 1.0 else 0.0)

    return {
        'Valleys': valleys,
        'Peaks': peaks
    }

def calculate_indicator(df, **params):
    """
    Wrapper function to calculate peaks and valleys.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        **params: Parameters to pass to calculate_peaks_valleys().

    Returns:
        dict: Dictionary with 'Valleys' and 'Peaks' columns.
    """
    return calculate_peaks_valleys(df, **params)
