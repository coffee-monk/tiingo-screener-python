import pandas as pd

def calculate_gaps(df):

    df['Prev_High'] = df['High'].shift(1)  # Previous high
    df['Prev_Low'] = df['Low'].shift(1)    # Previous low

    gap_up = (df['Low'] > df['Prev_High']).astype(int)
    gap_down = (df['High'] < df['Prev_Low']).astype(int)

    return {
        'Gap_Up': gap_up,
        'Gap_Down': gap_down,
    }

def calculate_indicator(df):
    return calculate_gaps(df)
