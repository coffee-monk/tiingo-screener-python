import pandas as pd

def calculate_peaks_valleys(df, window_size=25, **params):
    valleys = df['Low'].rolling(window_size, center=True).min() / df['Low']
    peaks = df['High'].rolling(window_size, center=True).max() / df['High']

    # Peaks/valleys = 1.0, else = 0.0
    valleys = valleys.apply(lambda x: 1.0 if x == 1.0 else 0.0)
    peaks = peaks.apply(lambda x: 1.0 if x == 1.0 else 0.0)

    print(peaks)

    return {
        'Valleys': valleys,
        'Peaks': peaks
    }

def calculate_indicator(df, **params):
    return calculate_peaks_valleys(df, **params)
