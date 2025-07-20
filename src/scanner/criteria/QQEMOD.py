import pandas as pd

def QQEMOD(
    df: pd.DataFrame,
    mode: str = 'overbought',
    min_consecutive: int = 3,
    require_confirmation: bool = True
) -> pd.DataFrame:
    """
    Unified QQEMOD scanner with multiple detection modes.
    
    Parameters:
        df: DataFrame with QQEMOD indicator columns
        mode: One of ['overbought', 'oversold', 'bullish_reversal', 'bearish_reversal']
        min_consecutive: Minimum consecutive candles required for reversal modes
        require_confirmation: Whether to require confirmation for reversal signals
        
    Returns:
        pd.DataFrame with detected signals (empty if none found)
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    result = None
    
    # Mode selection
    if mode == 'overbought':
        # Teal condition (strong bullish)
        conditions = (
            latest['QQE1_Above_Upper'] and
            latest['QQE2_Above_Threshold'] and
            latest['QQE2_Above_TL']
        )
        if conditions:
            result = latest.to_frame().T
            result['QQEMOD_Signal'] = 'Overbought'
            
    elif mode == 'oversold':
        # Red condition (strong bearish)
        conditions = (
            latest['QQE1_Below_Lower'] and
            latest['QQE2_Below_Threshold'] and
            not latest['QQE2_Above_TL']
        )
        if conditions:
            result = latest.to_frame().T
            result['QQEMOD_Signal'] = 'Oversold'
            
    elif mode == 'bearish_reversal':
        if len(df) >= min_consecutive + 1:
            window = df.iloc[-(min_consecutive+1):]
            current = window.iloc[-1]
            previous = window.iloc[:-1]
            
            # Current candle shows weakening
            current_cond = (
                current['QQE1_Above_Upper'] and
                current['QQE2_Above_Threshold'] and
                not current['QQE2_Above_TL']  # Difference from pure teal
            )
            
            # Previous candles were strong bullish
            prev_cond = all(
                (row['QQE1_Above_Upper'] and
                 row['QQE2_Above_Threshold'] and
                 row['QQE2_Above_TL'])
                for _, row in previous.iterrows()
            )
            
            if current_cond and prev_cond:
                result = current.to_frame().T
                result['QQEMOD_Signal'] = 'Bearish_Reversal'
                result['QQEMOD_Consecutive'] = len(previous)
                result['QQEMOD_Strength'] = (
                    1 if not current['QQE2_Above_TL'] and previous.iloc[-1]['QQE2_Above_TL']
                    else 0
                )
                
    elif mode == 'bullish_reversal':
        if len(df) >= min_consecutive + 1:
            window = df.iloc[-(min_consecutive+1):]
            current = window.iloc[-1]
            previous = window.iloc[:-1]
            
            # Current candle shows weakening bearish momentum
            current_cond = (
                current['QQE1_Below_Lower'] and
                current['QQE2_Below_Threshold'] and
                current['QQE2_Above_TL']  # Difference from pure red
            )
            
            # Previous candles were strong bearish
            prev_cond = all(
                (row['QQE1_Below_Lower'] and
                 row['QQE2_Below_Threshold'] and
                 not row['QQE2_Above_TL'])
                for _, row in previous.iterrows()
            )
            
            if current_cond and prev_cond:
                result = current.to_frame().T
                result['QQEMOD_Signal'] = 'Bullish_Reversal'
                result['QQEMOD_Consecutive'] = len(previous)
                result['QQEMOD_Strength'] = (
                    1 if current['QQE2_Above_TL'] and not previous.iloc[-1]['QQE2_Above_TL']
                    else 0
                )
    
    # Additional confirmation checks if required
    if require_confirmation and result is not None:
        if mode in ['bearish_reversal', 'bullish_reversal']:
            # For reversals, check if price action confirms
            if mode == 'bearish_reversal':
                if df['Close'].iloc[-1] > df['Close'].iloc[-2]:
                    return pd.DataFrame()  # Price going up invalidates bearish reversal
            else:
                if df['Close'].iloc[-1] < df['Close'].iloc[-2]:
                    return pd.DataFrame()  # Price going down invalidates bullish reversal
    
    return result if result is not None else pd.DataFrame()

def calculate_indicator(df, **params):
    """Wrapper function for consistent interface"""
    return scan_qqemod(df, **params)
