# import pandas as pd
# from typing import Optional, Literal
#
# def OB(
#     df: pd.DataFrame,
#     mode: Literal['bullish', 'bearish', 'support', 'resistance'] = 'bullish',
#     atr_threshold: Optional[float] = None,
#     max_lookback: Optional[int] = None
# ) -> pd.DataFrame:
#     """
#     Unified Order Block scanner with multiple detection modes.
#
#     Parameters:
#         df: DataFrame containing:
#             - 'OB' (-1=bearish, 0=neutral, 1=bullish)
#             - 'OB_High'/'OB_Low' (price range)
#             - 'Close' (current price)
#             - Optional 'ATR' if using threshold multiplier
#            
#         mode: Detection mode:
#             - 'bearish': Most recent OB is bearish
#             - 'bullish': Most recent OB is bullish
#             - 'support': Current price is within most recent bullish OB range
#             - 'resistance': Current price is within most recent bearish OB range
#            
#         atr_threshold: 
#             - None for exact OB range matching
#             - Float (e.g., 0.5) to expand range using ATR
#            
#         max_lookback: 
#             - Maximum bars to look back (None for all history)
#            
#     Returns:
#         Single-row DataFrame of matching OB, or empty if none found
#     """
#
#     if len(df) == 0:
#         return pd.DataFrame()
#
#     # Apply lookback window if specified
#     if max_lookback is not None:
#         df = df.iloc[-max_lookback:]
#
#     # Basic OB detection modes
#     if mode in ['bearish', 'bullish']:
#         # First find the most recent non-zero OB (bullish or bearish)
#         reversed_df = df.iloc[::-1]
#         recent_ob = reversed_df[reversed_df['OB'] != 0].head(1)
#        
#         # Then check if it matches our requested mode
#         if not recent_ob.empty:
#             ob_value = recent_ob.iloc[0]['OB']
#             if (mode == 'bullish' and ob_value == 1) or (mode == 'bearish' and ob_value == -1):
#                 return recent_ob
#        
#         return pd.DataFrame()
#
#     # Price-proximity modes (STRICT most recent OB check)
#     elif mode in ['support', 'resistance']:
#         current_price = df['Close'].iloc[-1]
#         target_value = 1 if mode == 'support' else -1
#        
#         # Find the SINGLE MOST RECENT OB of target type
#         reversed_df = df.iloc[::-1]
#         most_recent_ob = reversed_df[reversed_df['OB'] == target_value].head(1)
#        
#         if most_recent_ob.empty:
#             return pd.DataFrame()
#        
#         # Calculate tolerance if using ATR
#         ob = most_recent_ob.iloc[0]
#         tolerance = 0.0
#         if atr_threshold is not None:
#             if 'ATR' not in df.columns:
#                 df = df.copy()
#                 df['ATR'] = _calculate_atr(df)
#             tolerance = df['ATR'].iloc[-1] * atr_threshold
#        
#         # Check current price against OB range (±tolerance)
#         ob_low = ob['OB_Low'] - tolerance
#         ob_high = ob['OB_High'] + tolerance
#        
#         if ob_low <= current_price <= ob_high:
#             return pd.DataFrame([ob])
#         return pd.DataFrame()
#
#     else:
#         raise ValueError(f"Invalid mode: {mode}. Must be 'bearish', 'bullish', 'support', or 'resistance'")
#
# def _calculate_atr(df: pd.DataFrame, length: int = 7) -> pd.Series:
#     """Internal ATR calculation for support/resistance tolerance"""
#     high = df['High']
#     low = df['Low']
#     close = df['Close']
#    
#     tr1 = high - low
#     tr2 = abs(high - close.shift(1))
#     tr3 = abs(low - close.shift(1))
#     tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
#    
#     atr = tr.rolling(length).mean()
#     atr[length:] = tr.ewm(span=length, adjust=False).mean()[length:]
#     return atr
#
# def calculate_indicator(df, **params):
#     """Standard interface wrapper"""
#     return OB(df, **params)





import pandas as pd
from typing import Optional, Literal

def OB(
    df: pd.DataFrame,
    mode: Literal['bullish', 'bearish', 'support', 'resistance'] = 'bullish',
    atr_threshold: Optional[float] = None,
    max_lookback: Optional[int] = None,
    stdev_threshold: Optional[float] = None,
    stdev_mode: Literal['overbought', 'oversold'] = 'overbought'
) -> pd.DataFrame:
    """
    Simplified Order Block scanner with standard deviation filtering.
    
    Parameters:
        df: DataFrame containing:
            - 'OB' (-1=bearish, 0=neutral, 1=bullish)
            - 'OB_High'/'OB_Low' (price range)
            - 'Close' (current price)
            - 'StDev_Mean' (centerline)
            - 'StDev' (standard deviation)
            - Optional 'ATR' if using threshold multiplier
            
        mode: Detection mode:
            - 'bullish': Most recent OB is bullish
            - 'bearish': Most recent OB is bearish  
            - 'support': Price within most recent bullish OB range
            - 'resistance': Price within most recent bearish OB range
            
        atr_threshold: 
            - None for exact OB range matching
            - Float to expand range using ATR (e.g., 0.5)
            
        max_lookback: 
            - Maximum bars to look back (None for all history)
            
        stdev_threshold: 
            - None to disable standard deviation filtering
            - Float for how many StDevs from mean (e.g., 2.0)
            
        stdev_mode:
            - 'overbought': OB was overbought (price above StDev band)
            - 'oversold': OB was oversold (price below StDev band)
            
    Returns:
        pd.DataFrame: Single-row DataFrame of matching OB, or empty if none found
    """

    if len(df) == 0:
        return pd.DataFrame()

    # Apply lookback window if specified
    if max_lookback is not None:
        df = df.iloc[-max_lookback:]

    # Basic OB detection modes
    if mode in ['bearish', 'bullish']:
        # Find the most recent non-zero OB (bullish or bearish)
        reversed_df = df.iloc[::-1]
        recent_ob = reversed_df[reversed_df['OB'] != 0].head(1)
        
        # Check if it matches our requested mode
        if not recent_ob.empty:
            ob_value = recent_ob.iloc[0]['OB']
            if (mode == 'bullish' and ob_value == 1) or (mode == 'bearish' and ob_value == -1):
                # Check standard deviation condition if threshold provided
                if stdev_threshold is not None:
                    ob_row = recent_ob.iloc[0]
                    if _check_stdev_condition(ob_row, stdev_threshold, stdev_mode):
                        return recent_ob
                    return pd.DataFrame()
                return recent_ob
        
        return pd.DataFrame()

    # Price-proximity modes
    elif mode in ['support', 'resistance']:
        current_price = df['Close'].iloc[-1]
        target_value = 1 if mode == 'support' else -1
        
        # Find the most recent OB of target type
        reversed_df = df.iloc[::-1]
        most_recent_ob = reversed_df[reversed_df['OB'] == target_value].head(1)
        
        if most_recent_ob.empty:
            return pd.DataFrame()
        
        # Check standard deviation condition if threshold provided
        ob = most_recent_ob.iloc[0]
        if stdev_threshold is not None:
            if not _check_stdev_condition(ob, stdev_threshold, stdev_mode):
                return pd.DataFrame()
        
        # Calculate tolerance if using ATR
        tolerance = 0.0
        if atr_threshold is not None:
            if 'ATR' not in df.columns:
                df = df.copy()
                df['ATR'] = _calculate_atr(df)
            tolerance = df['ATR'].iloc[-1] * atr_threshold
        
        # Check current price against OB range (±tolerance)
        ob_low = ob['OB_Low'] - tolerance
        ob_high = ob['OB_High'] + tolerance
        
        if ob_low <= current_price <= ob_high:
            return pd.DataFrame([ob])
        return pd.DataFrame()

    else:
        raise ValueError(f"Invalid mode: {mode}")

def _check_stdev_condition(ob_row: pd.Series, threshold: float, mode: str) -> bool:
    """
    Check if OB meets standard deviation condition.
    """
    if 'StDev_Mean' not in ob_row.index or 'StDev' not in ob_row.index:
        return False
    
    stdev_mean = ob_row['StDev_Mean']
    stdev = ob_row['StDev']
    
    if mode == 'oversold':
        # Price was significantly below mean (oversold condition)
        return ob_row['Close'] < (stdev_mean - threshold * stdev)
    elif mode == 'overbought':
        # Price was significantly above mean (overbought condition)
        return ob_row['Close'] > (stdev_mean + threshold * stdev)
    else:
        return False

def _calculate_atr(df: pd.DataFrame, length: int = 7) -> pd.Series:
    """Internal ATR calculation for support/resistance tolerance"""
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    atr = tr.rolling(length).mean()
    atr[length:] = tr.ewm(span=length, adjust=False).mean()[length:]
    return atr

def calculate_indicator(df, **params):
    """Standard interface wrapper"""
    return OB(df, **params)
