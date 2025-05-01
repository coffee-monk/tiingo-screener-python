import pandas as pd

def calculate_mfi_divergence(df, period=14, lookback=5, volume_threshold=1.2):
    """
    Advanced MFI Divergence with Volume Confirmation
    Returns:
    {
        'MFI': Raw MFI values,
        'MFI_Regular_Bullish',
        'MFI_Regular_Bearish', 
        'MFI_Hidden_Bullish',
        'MFI_Hidden_Bearish',
        'MFI_Volume_Confirmation'
    }
    """
    # 1. Calculate Money Flow Index
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    money_flow = typical_price * df['Volume']
    
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    
    pos_flow_sum = positive_flow.rolling(period).sum()
    neg_flow_sum = negative_flow.rolling(period).sum()
    
    mfi = 100 * (pos_flow_sum / (pos_flow_sum + neg_flow_sum))
    
    # 2. Volume-Weighted MFI (Unique Enhancement)
    vol_ema = df['Volume'].ewm(span=period).mean()
    weighted_mfi = mfi * (df['Volume'] / vol_ema)
    
    # 3. Divergence Detection
    regular_bullish = (
        (df['Close'].rolling(lookback).min() == df['Close']) & 
        (df['Close'] < df['Close'].shift(lookback)) &
        (weighted_mfi > weighted_mfi.shift(lookback)) &
        (mfi < 30)  # Oversold filter
    )
    
    regular_bearish = (
        (df['Close'].rolling(lookback).max() == df['Close']) & 
        (df['Close'] > df['Close'].shift(lookback)) &
        (weighted_mfi < weighted_mfi.shift(lookback)) &
        (mfi > 70)  # Overbought filter
    )
    
    # 4. Hidden Divergences (Trend Continuation)
    hidden_bullish = (
        (df['Close'].rolling(lookback).min() == df['Close']) & 
        (df['Close'] > df['Close'].shift(lookback)) &
        (weighted_mfi < weighted_mfi.shift(lookback)) &
        (mfi > 50)  # Bullish trend filter
    )
    
    hidden_bearish = (
        (df['Close'].rolling(lookback).max() == df['Close']) & 
        (df['Close'] < df['Close'].shift(lookback)) &
        (weighted_mfi > weighted_mfi.shift(lookback)) &
        (mfi < 50)  # Bearish trend filter
    )
    
    # 5. Volume Confirmation (New Feature)
    volume_conf = (df['Volume'] > vol_ema * volume_threshold)
    
    return {
        'MFI': mfi,
        'MFI_Weighted': weighted_mfi,
        'MFI_Regular_Bullish': regular_bullish & volume_conf,
        'MFI_Regular_Bearish': regular_bearish & volume_conf,
        'MFI_Hidden_Bullish': hidden_bullish & volume_conf,
        'MFI_Hidden_Bearish': hidden_bearish & volume_conf,
        'MFI_Volume_Confirmation': volume_conf
    }

def calculate_indicator(df, **params):
    return calculate_mfi_divergence(df, **params)
