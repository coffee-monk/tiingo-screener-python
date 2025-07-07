import pandas as pd

def QQEMOD_bearish_reversal(df, min_teal_candles=3):
    """
    Scans for potential bearish reversals after an uptrend.
    
    Conditions:
    1. Current candle is teal_trans_3 (weakening bullish momentum)
    2. At least N consecutive pure teal candles before it
    3. The pure teal candles showed strong bullish conditions
    
    Parameters:
        df: DataFrame with QQEMOD columns
        min_teal_candles: Minimum consecutive teal candles required (default: 3)
    
    Returns:
        pd.DataFrame: Latest row if reversal conditions met, else empty
    """
    if len(df) < min_teal_candles + 1:
        return pd.DataFrame()
    
    window = df.iloc[-(min_teal_candles+1):]
    current = window.iloc[-1]
    previous_teals = window.iloc[:-1]
    
    # Current candle must be teal_trans_3 (weakening)
    current_condition = (
        current['QQE1_Above_Upper'] and 
        current['QQE2_Above_Threshold'] and 
        not current['QQE2_Above_TL']  # Difference from pure teal
    )
    
    # Previous candles must be pure teal (strong bullish)
    previous_conditions = all(
        (row['QQE1_Above_Upper'] and 
         row['QQE2_Above_Threshold'] and 
         row['QQE2_Above_TL'])  # Pure teal
        for _, row in previous_teals.iterrows()
    )
    
    if current_condition and previous_conditions:
        result = current.to_frame().T
        result['QQEMOD_Teal_Count'] = len(previous_teals)
        
        # Momentum shift calculation (1 if weakening)
        result['QQEMOD_Reversal_Strength'] = (
            1 if not current['QQE2_Above_TL'] and previous_teals.iloc[-1]['QQE2_Above_TL']
            else 0
        )
        return result
    
    return pd.DataFrame()
