import pandas as pd

def div_Fisher_bullish(
    df: pd.DataFrame,
    max_bars_back: int = 20,  # How far back to check for divergences
    require_confirmation: bool = True,  # Wait for 1-2 bars of confirmation
) -> pd.DataFrame:
    """
    Scan for the most recent Fisher Transform bullish divergence (regular or hidden).
    
    Returns:
        - Latest row if most recent Fisher divergence was bullish and still active
        - Empty DataFrame otherwise
    """
    if len(df) < 2:
        return pd.DataFrame()

    # 1. Find most recent Fisher bullish divergence
    divergence_indices = []
    fisher_bullish_columns = [
        'Fisher_Regular_Bullish',
        'Fisher_Hidden_Bullish'
    ]
    
    for col in fisher_bullish_columns:
        if col in df.columns:
            last_divergence = df[df[col]].index[-1] if df[col].any() else None
            if last_divergence is not None:
                divergence_indices.append(last_divergence)
    
    if not divergence_indices:
        return pd.DataFrame()  # No Fisher divergence found
    
    most_recent_divergence_idx = max(divergence_indices)
    divergence_row = df.loc[most_recent_divergence_idx]

    # 2. Check for newer bearish signals
    fisher_bearish_columns = [
        'Fisher_Regular_Bearish',
        'Fisher_Hidden_Bearish'
    ]
    
    newer_bearish = False
    for col in fisher_bearish_columns:
        if col in df.columns:
            if df.loc[most_recent_divergence_idx:][col].any():
                newer_bearish = True
                break

    # 3. Price confirmation check
    if require_confirmation:
        if df.loc[most_recent_divergence_idx:]['Low'].min() < divergence_row['Low']:
            return pd.DataFrame()  # Divergence invalidated

    # 4. Return signal if still valid
    if not newer_bearish:
        return df.iloc[-1:].copy()
    
    return pd.DataFrame()

def calculate_indicator(df, **params):
    return div_Fisher_bullish(df, **params)
