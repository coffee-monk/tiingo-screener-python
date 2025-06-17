import pandas as pd

def calculate_ttm_squeeze(
                          df,
                          bb_length=20,
                          bb_std_dev=2.0,
                          kc_length=20,
                          kc_mult=1.5,
                          use_true_range=True
                         ):
    """
    Simplified TTM Squeeze Indicator (Volatility Focus)
    
    Parameters:
        df (pd.DataFrame): Must contain columns ['High', 'Low', 'Close']
        bb_length (int): Bollinger Bands lookback period (default: 20)
        bb_std_dev (float): BB standard deviation multiplier (default: 2.0)
        kc_length (int): Keltner Channel lookback period (default: 20)
        kc_mult (float): KC ATR multiplier (default: 1.5)
        use_true_range (bool): Use True Range for KC (default: True)
        
    Returns:
        dict: {
            'squeeze_on': (pd.Series) Binary squeeze status [1=active, 0=inactive],
            'bb_upper': (pd.Series) Bollinger Band upper values,
            'bb_lower': (pd.Series) Bollinger Band lower values,
            'kc_upper': (pd.Series) Keltner Channel upper values,
            'kc_lower': (pd.Series) Keltner Channel lower values,
            'basis': (pd.Series) Bollinger Band moving average
        }
    """
    # Bollinger Bands Calculation
    basis = df['Close'].rolling(bb_length).mean()
    std_dev = df['Close'].rolling(bb_length).std()
    bb_upper = basis + (std_dev * bb_std_dev)
    bb_lower = basis - (std_dev * bb_std_dev)
    
    # Keltner Channels Calculation
    if use_true_range:
        tr = pd.concat([
            df['High'] - df['Low'],
            abs(df['High'] - df['Close'].shift()),
            abs(df['Low'] - df['Close'].shift())
        ], axis=1).max(axis=1)
        atr = tr.rolling(kc_length).mean()
    else:
        atr = (df['High'] - df['Low']).rolling(kc_length).mean()
    
    kc_middle = df['Close'].ewm(span=kc_length, adjust=False).mean()
    kc_upper = kc_middle + (atr * kc_mult)
    kc_lower = kc_middle - (atr * kc_mult)
    
    # Squeeze Detection
    squeeze_on = (bb_upper < kc_upper) & (bb_lower > kc_lower)
    
    return {
        'TTM_squeeze_Active': squeeze_on.astype(int),
        # 'TTM_BB_upper': bb_upper,
        # 'TTM_BB_lower': bb_lower,
        # 'TTM_KC_upper': kc_upper,
        # 'TTM_KC_lower': kc_lower,
        # 'TTM_basis': basis
    }

def calculate_indicator(df, **params):
    """Standardized wrapper function"""
    return calculate_ttm_squeeze(df, **params)
