import numpy as np

def calculate_fractal_divergence(df, period=12, vol_filter=True):
    hl_range = (df['High'] - df['Low']).rolling(period)
    close_range = df['Close'].diff(period).abs()
    energy = (close_range / hl_range.mean()).replace(np.inf, 0)
    
    signals = {
        'Fractal_Energy': energy,
        'Fractal_Bullish': (
            (df['Close'] < df['Close'].shift(period)) & 
            (energy > energy.rolling(period).mean() * 1.5)
        ),
        'Fractal_Bearish': (
            (df['Close'] > df['Close'].shift(period)) & 
            (energy < energy.rolling(period).mean() * 0.67)
        )
    }
    
    if vol_filter:
        signals['Fractal_Bullish'] &= (df['Volume'] > df['Volume'].ewm(span=20).mean()*1.2)
        signals['Fractal_Bearish'] &= (df['Volume'] > df['Volume'].ewm(span=20).mean()*1.2)
    
    return {
        'Fractal_Bullish': signals['Fractal_Bullish'],
        'Fractal_Bearish': signals['Fractal_Bearish'],
    }

def calculate_indicator(df, **params):
    return calculate_fractal_divergence(df, **params)
