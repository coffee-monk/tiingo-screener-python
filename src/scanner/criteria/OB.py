# import pandas as pd
# from typing import Optional, Literal
#
# def OB(
#     df: pd.DataFrame,
#     mode: Literal['bearish', 'bullish', 'support', 'resistance'] = 'bullish',
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
#             - 'support': Bullish OB near current price
#             - 'resistance': Bearish OB near current price
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
#     # Price-proximity modes
#     elif mode in ['support', 'resistance']:
#         current_price = df['Close'].iloc[-1]
#         target_value = 1 if mode == 'support' else -1
#        
#         # Calculate tolerance if using ATR
#         tolerance = 0.0
#         if atr_threshold is not None:
#             if 'ATR' not in df.columns:
#                 df = df.copy()
#                 df['ATR'] = _calculate_atr(df)
#             tolerance = df['ATR'].iloc[-1] * atr_threshold
#
#         # Search most recent to oldest
#         for i in range(len(df)-1, -1, -1):
#             if df['OB'].iloc[i] == target_value:
#                 ob = df.iloc[i]
#                 low = ob['OB_Low'] - tolerance
#                 high = ob['OB_High'] + tolerance
#                
#                 if low <= current_price <= high:
#                     return pd.DataFrame([ob])
#                 break
#        
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
    max_lookback: Optional[int] = None
) -> pd.DataFrame:
    """
    Unified Order Block scanner with multiple detection modes.
    
    Parameters:
        df: DataFrame containing:
            - 'OB' (-1=bearish, 0=neutral, 1=bullish)
            - 'OB_High'/'OB_Low' (price range)
            - 'Close' (current price)
            - Optional 'ATR' if using threshold multiplier
            
        mode: Detection mode:
            - 'bearish': Most recent OB is bearish
            - 'bullish': Most recent OB is bullish
            - 'support': Current price is within most recent bullish OB range
            - 'resistance': Current price is within most recent bearish OB range
            
        atr_threshold: 
            - None for exact OB range matching
            - Float (e.g., 0.5) to expand range using ATR
            
        max_lookback: 
            - Maximum bars to look back (None for all history)
            
    Returns:
        Single-row DataFrame of matching OB, or empty if none found
    """
    if len(df) == 0:
        return pd.DataFrame()

    # Apply lookback window if specified
    if max_lookback is not None:
        df = df.iloc[-max_lookback:]

    # Basic OB detection modes
    if mode in ['bearish', 'bullish']:
        # First find the most recent non-zero OB (bullish or bearish)
        reversed_df = df.iloc[::-1]
        recent_ob = reversed_df[reversed_df['OB'] != 0].head(1)
        
        # Then check if it matches our requested mode
        if not recent_ob.empty:
            ob_value = recent_ob.iloc[0]['OB']
            if (mode == 'bullish' and ob_value == 1) or (mode == 'bearish' and ob_value == -1):
                return recent_ob
        
        return pd.DataFrame()

    # Price-proximity modes (STRICT most recent OB check)
    elif mode in ['support', 'resistance']:
        current_price = df['Close'].iloc[-1]
        target_value = 1 if mode == 'support' else -1
        
        # Find the SINGLE MOST RECENT OB of target type
        reversed_df = df.iloc[::-1]
        most_recent_ob = reversed_df[reversed_df['OB'] == target_value].head(1)
        
        if most_recent_ob.empty:
            return pd.DataFrame()
        
        # Calculate tolerance if using ATR
        ob = most_recent_ob.iloc[0]
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
        raise ValueError(f"Invalid mode: {mode}. Must be 'bearish', 'bullish', 'support', or 'resistance'")

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
