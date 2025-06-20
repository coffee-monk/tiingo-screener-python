import pandas as pd

def TTM_squeeze(df, mode='active', min_squeeze_bars=5, max_squeeze_bars=None):
    """
    Enhanced TTM Squeeze scanner with duration tracking
    
    Parameters:
        df (pd.DataFrame): Must contain 'TTM_squeeze_Active' column
        mode: 'active' or 'breakout' - which condition to check
        min_squeeze_bars: Minimum consecutive squeeze bars required
        max_squeeze_bars: Maximum allowed squeeze bars (optional)
            
    Returns:
        pd.DataFrame: Single-row with metadata if condition met, else empty
    """
    if len(df) == 0 or 'TTM_squeeze_Active' not in df.columns:
        return pd.DataFrame()
    
    # Calculate squeeze duration (consecutive squeeze bars)
    squeeze_changes = (df['TTM_squeeze_Active'].diff() != 0).cumsum()
    df['squeeze_duration'] = df.groupby(squeeze_changes)['TTM_squeeze_Active'].cumsum()
    
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else None
    
    result = pd.DataFrame()
    
    if mode == 'active':
        if (latest['TTM_squeeze_Active'] == 1 and 
            latest['squeeze_duration'] >= min_squeeze_bars):
            if max_squeeze_bars is None or latest['squeeze_duration'] <= max_squeeze_bars:
                result = pd.DataFrame([{
                    'timestamp': latest.name,
                    'close': latest['Close'],
                    'squeeze_duration': latest['squeeze_duration'],
                    'status': 'active'
                }])
                
    elif mode == 'breakout':
        if (prev is not None and 
            prev['TTM_squeeze_Active'] == 1 and 
            latest['TTM_squeeze_Active'] == 0 and
            prev['squeeze_duration'] >= min_squeeze_bars):
            result = pd.DataFrame([{
                'timestamp': latest.name,
                'close': latest['Close'],
                'squeeze_duration': prev['squeeze_duration'],
                'status': 'breakout'
            }])
    
    return result
