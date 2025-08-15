import pandas as pd
from typing import Literal

def BoS_CHoCH(
    df: pd.DataFrame,
    mode: Literal['BoS_bullish', 'BoS_bearish', 'CHoCH_bullish', 'CHoCH_bearish'],
    lookback_bars: int = 200
) -> pd.DataFrame:
    """
    Break of Structure (BoS) and Change of Character (CHoCH) scanner.
    
    Parameters:
        df: DataFrame containing BoS/CHoCH columns from indicator calculation
        mode: Detection mode:
            - 'BoS_bullish': Most recent BoS is bullish
            - 'BoS_bearish': Most recent BoS is bearish  
            - 'CHoCH_bullish': Most recent CHoCH is bullish
            - 'CHoCH_bearish': Most recent CHoCH is bearish
        lookback_bars: Number of bars to look back for events
    
    Returns:
        Single-row DataFrame if most recent event matches criteria, else empty DataFrame
    """
    if len(df) < lookback_bars:
        return pd.DataFrame()
    
    # Verify required columns exist
    required_cols = ['BoS', 'CHoCH', 'Close']
    if not all(col in df.columns for col in required_cols):
        return pd.DataFrame()
    
    # Determine event type and direction from mode
    event_type = 'BoS' if 'BoS' in mode else 'CHoCH'
    target_direction = 1 if 'bullish' in mode else -1
    
    # Slice the lookback window (excluding current candle)
    lookback_df = df.iloc[-(lookback_bars+1):-1] if len(df) > lookback_bars else df.iloc[:-1]
    
    # Find the MOST RECENT event (of any type/direction)
    last_event_type = None
    last_event_direction = None
    last_event_index = -1
    
    # Search from most recent to oldest
    for i in range(len(lookback_df)-1, -1, -1):
        row = lookback_df.iloc[i]
        if row['BoS'] != 0:  # Found a BoS event
            last_event_type = 'BoS'
            last_event_direction = row['BoS']
            last_event_index = i
            break
        elif row['CHoCH'] != 0:  # Found a CHoCH event
            last_event_type = 'CHoCH'
            last_event_direction = row['CHoCH']
            last_event_index = i
            break
    
    # Check if the most recent event matches our criteria
    if (last_event_type == event_type and 
        last_event_direction == target_direction):
        
        # Prepare results
        result = df.iloc[-1:].copy()
        result['Event_Type'] = event_type
        result['Event_Direction'] = 'Bullish' if target_direction == 1 else 'Bearish'
        result['Bars_Since_Event'] = len(lookback_df) - last_event_index
        return result
    
    return pd.DataFrame()

def calculate_indicator(df, **params):
    """Standard interface wrapper"""
    return BoS_CHoCH(df, **params)
