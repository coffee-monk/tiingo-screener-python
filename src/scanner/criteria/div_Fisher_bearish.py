import pandas as pd

def div_Fisher_bearish(
    df: pd.DataFrame,
    max_bars_back: int = 20,
    require_confirmation: bool = True,
) -> pd.DataFrame:
    """
    Scan for the most recent Fisher Transform bearish divergence (regular or hidden).
    """
    if len(df) < 2:
        return pd.DataFrame()

    # 1. Find most recent Fisher bearish divergence
    divergence_indices = []
    fisher_bearish_columns = [
        'Fisher_Regular_Bearish', 
        'Fisher_Hidden_Bearish'
    ]
    
    for col in fisher_bearish_columns:
        if col in df.columns:
            last_divergence = df[df[col]].index[-1] if df[col].any() else None
            if last_divergence is not None:
                divergence_indices.append(last_divergence)
    
    if not divergence_indices:
        return pd.DataFrame()
    
    most_recent_divergence_idx = max(divergence_indices)
    divergence_row = df.loc[most_recent_divergence_idx]

    # 2. Check for newer bullish signals
    fisher_bullish_columns = [
        'Fisher_Regular_Bullish',
        'Fisher_Hidden_Bullish'
    ]
    
    newer_bullish = False
    for col in fisher_bullish_columns:
        if col in df.columns:
            if df.loc[most_recent_divergence_idx:][col].any():
                newer_bullish = True
                break

    # 3. Price confirmation check
    if require_confirmation:
        if df.loc[most_recent_divergence_idx:]['High'].max() > divergence_row['High']:
            return pd.DataFrame()

    # 4. Return signal if still valid
    if not newer_bullish:
        return df.iloc[-1:].copy()
    
    return pd.DataFrame()

def calculate_indicator(df, **params):
    return div_Fisher_bearish(df, **params)
