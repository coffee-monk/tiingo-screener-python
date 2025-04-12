import pandas as pd
from ta.momentum import RSIIndicator

def calculate_indicator(df, rsi_period=50, rsi_base=50, sensitivity=1.5):

    rsi = RSIIndicator(df['Close'], window=rsi_period).rsi() # Calculate RSI
    
    modified_rsi = sensitivity * (rsi - rsi_base) # Apply sensitivity & adjustment
    modified_rsi = modified_rsi.clip(lower=0, upper=20) # Clamp between 0 - 20

    return modified_rsi
