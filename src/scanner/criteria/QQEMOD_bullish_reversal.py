import pandas as pd

def QQEMOD_bullish_reversal(df, min_red_candles=3):
    """
    Scans for potential reversals after a pullback.
    """
    if len(df) < min_red_candles + 1:
        return pd.DataFrame()
    
    window = df.iloc[-(min_red_candles+1):]
    current = window.iloc[-1]
    previous_reds = window.iloc[:-1]
    
    current_condition = (
        current['QQE1_Below_Lower'] and 
        current['QQE2_Below_Threshold'] and 
        current['QQE2_Above_TL']
    )
    
    previous_conditions = all(
        (row['QQE1_Below_Lower'] and 
         row['QQE2_Below_Threshold'] and 
         not row['QQE2_Above_TL'])
        for _, row in previous_reds.iterrows()
    )
    
    if current_condition and previous_conditions:
        result = current.to_frame().T
        result['QQEMOD_Red_Count'] = len(previous_reds)
        
        # Safe calculation of momentum shift
        result['QQEMOD_Reversal_Strength'] = (
            1 if current['QQE2_Above_TL'] and not previous_reds.iloc[-1]['QQE2_Above_TL'] 
            else 0
        )
        return result
    
    return pd.DataFrame()
