import pandas as pd
import numpy as np

def calculate_qqemod(
    df,
    rsi_period=6,
    rsi_period2=6,
    sf=5,
    sf2=5,
    qqe_factor=3.0,
    qqe_factor2=1.61,
    threshold=3,
    bb_length=50,
    bb_multi=0.35,
):
    """
    Calculates the QQEMOD indicator with two QQE signals and Bollinger Band filtering.
    
    Parameters:
        df : pd.DataFrame with 'Close' column
        
        # Primary QQE Signal
        rsi_period : int (default: 6) - QQE1 RSI period
        sf : int (default: 5) - QQE1 smoothing factor
        qqe_factor : float (default: 3.0) - QQE1 multiplier
        
        # Secondary QQE Signal
        rsi_period2 : int (default: 6) - QQE2 RSI period
        sf2 : int (default: 5) - QQE2 smoothing factor
        qqe_factor2 : float (default: 1.61) - QQE2 multiplier

        threshold : float (default: 3) - Used for QQE2 signal conditions
        
        # Bollinger Band Filter
        bb_length : int (default: 50) - BB length
        bb_mult : float (default: 0.35) - BB standard deviation multiplier
    
    Returns:
        dict with components for candle coloring:
        {
            'QQEMOD', 'QQE1_Value', 
            'QQE1_Above_Upper', 'QQE1_Below_Lower',
            'QQE2_Above_Threshold', 'QQE2_Below_Threshold', 'QQE2_Above_TL'
        }
    """

    # QQE1 Calculation (Primary Signal) ---------------------------------------

    wilders_period = rsi_period * 2 - 1
    
    # Wilder's RSI Calculation
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.ewm(alpha=1/wilders_period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/wilders_period, adjust=False).mean()
    rsi = 100 - (100 / (1 + (avg_gain / avg_loss)))
    
    # Smooth RSI with EMA
    rsi_ma = rsi.ewm(span=sf, adjust=False).mean()
    
    # ATR of RSI (Double EMA)
    atr_rsi = np.abs(rsi_ma.diff())
    ma_atr_rsi = atr_rsi.ewm(span=wilders_period, adjust=False).mean()
    dar = ma_atr_rsi.ewm(span=wilders_period, adjust=False).mean() * qqe_factor
    
    # Dynamic Bands Calculation
    longband = pd.Series(np.nan, index=df.index)
    shortband = pd.Series(np.nan, index=df.index)
    trend = pd.Series(1, index=df.index)  # Default to uptrend
    
    for i in range(1, len(df)):
        rs_index = rsi_ma.iloc[i]
        prev_rs_index = rsi_ma.iloc[i-1]
        
        new_longband = rs_index - dar.iloc[i]
        new_shortband = rs_index + dar.iloc[i]
        
        # Longband logic
        if prev_rs_index > longband.iloc[i-1] and rs_index > longband.iloc[i-1]:
            longband.iloc[i] = max(longband.iloc[i-1], new_longband)
        else:
            longband.iloc[i] = new_longband
        
        # Shortband logic
        if prev_rs_index < shortband.iloc[i-1] and rs_index < shortband.iloc[i-1]:
            shortband.iloc[i] = min(shortband.iloc[i-1], new_shortband)
        else:
            shortband.iloc[i] = new_shortband
        
        # Trend detection
        if rs_index > shortband.iloc[i-1]:
            trend.iloc[i] = 1
        elif rs_index < longband.iloc[i-1]:
            trend.iloc[i] = -1
        else:
            trend.iloc[i] = trend.iloc[i-1]
    
    fast_atr_rsi_tl = np.where(trend == 1, longband, shortband)
    
    # Convert to pandas Series for rolling calculations
    fast_atr_rsi_tl_series = pd.Series(fast_atr_rsi_tl, index=df.index)
    
    # Bollinger Bands Filter (fixed)
    basis = (fast_atr_rsi_tl_series - 50).rolling(bb_length).mean()
    dev = bb_multi * (fast_atr_rsi_tl_series - 50).rolling(bb_length).std()
    upper_bb = basis + dev
    lower_bb = basis - dev
    
    # QQE2 Calculation (Secondary Signal) -------------------------------------

    wilders_period2 = rsi_period2 * 2 - 1
    
    # RSI Calculation for QQE2
    delta2 = df['Close'].diff()
    gain2 = delta2.where(delta2 > 0, 0)
    loss2 = -delta2.where(delta2 < 0, 0)
    
    avg_gain2 = gain2.ewm(alpha=1/wilders_period2, adjust=False).mean()
    avg_loss2 = loss2.ewm(alpha=1/wilders_period2, adjust=False).mean()
    rsi2 = 100 - (100 / (1 + (avg_gain2 / avg_loss2)))
    
    # Smooth RSI with EMA
    rsi_ma2 = rsi2.ewm(span=sf2, adjust=False).mean()
    
    # ATR of RSI for QQE2
    atr_rsi2 = np.abs(rsi_ma2.diff())
    ma_atr_rsi2 = atr_rsi2.ewm(span=wilders_period2, adjust=False).mean()
    dar2 = ma_atr_rsi2.ewm(span=wilders_period2, adjust=False).mean() * qqe_factor2
    
    # Dynamic Bands for QQE2
    longband2 = pd.Series(np.nan, index=df.index)
    shortband2 = pd.Series(np.nan, index=df.index)
    trend2 = pd.Series(1, index=df.index)
    
    for i in range(1, len(df)):
        rs_index2 = rsi_ma2.iloc[i]
        prev_rs_index2 = rsi_ma2.iloc[i-1]
        
        new_longband2 = rs_index2 - dar2.iloc[i]
        new_shortband2 = rs_index2 + dar2.iloc[i]
        
        if prev_rs_index2 > longband2.iloc[i-1] and rs_index2 > longband2.iloc[i-1]:
            longband2.iloc[i] = max(longband2.iloc[i-1], new_longband2)
        else:
            longband2.iloc[i] = new_longband2
        
        if prev_rs_index2 < shortband2.iloc[i-1] and rs_index2 < shortband2.iloc[i-1]:
            shortband2.iloc[i] = min(shortband2.iloc[i-1], new_shortband2)
        else:
            shortband2.iloc[i] = new_shortband2
        
        if rs_index2 > shortband2.iloc[i-1]:
            trend2.iloc[i] = 1
        elif rs_index2 < longband2.iloc[i-1]:
            trend2.iloc[i] = -1
        else:
            trend2.iloc[i] = trend2.iloc[i-1]
    
    fast_atr_rsi2_tl = np.where(trend2 == 1, longband2, shortband2)

    # QQEMOD Percent
    qqe_pct = 100 * (rsi_ma - lower_bb) / (upper_bb - lower_bb)
    
    # Prepare Output for Candle Coloring --------------------------------------

    return {
        # QQEMOD
        'QQEMOD': rsi_ma,
        # 'QQE_Pct': qqe_pct,

        # -- QQE1 Components --
        'QQE1_Value': fast_atr_rsi_tl - 50,  # Centered around 0
        # 'QQE1_RSI_MA': rsi_ma,
        # 'QQE1_Trend': trend,
        # 'QQE1_UpperBB': upper_bb,
        # 'QQE1_LowerBB': lower_bb,
        
        # -- QQE2 Components --
        # 'QQE2_Value': rsi_ma2 - 50,  # Centered around 0
        # 'QQE2_RSI_MA': rsi_ma2,
        # 'QQE2_Trend': trend2,
        
        # -- Derived Values --
        'QQE1_Above_Upper': (rsi_ma - 50) > upper_bb,
        'QQE1_Below_Lower': (rsi_ma - 50) < lower_bb,
        'QQE2_Above_Threshold': (rsi_ma2 - 50) > threshold,
        'QQE2_Below_Threshold': (rsi_ma2 - 50) < -threshold,
        'QQE2_Above_TL': rsi_ma2 >= fast_atr_rsi2_tl
    }

def calculate_indicator(df, **params):
    """Wrapper function for consistent interface"""
    return calculate_qqemod(df, **params)
