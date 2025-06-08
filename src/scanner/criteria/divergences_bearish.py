import pandas as pd

def divergences_bearish(
    df: pd.DataFrame,
    max_bars_back: int = 20,  # How far back to check for divergences
    require_confirmation: bool = True,  # Wait for 1-2 bars of confirmation
) -> pd.DataFrame:
    """
    Scan for the most recent bearish divergence (if any) and check if it's still valid.
    
    Returns:
        - Latest row if the most recent divergence was bearish and still active.
        - Empty DataFrame otherwise.
    """
    if len(df) < 2:
        return pd.DataFrame()

    # 1. Find the most recent bearish divergence (regular or hidden)
    divergence_indices = []
    
    # Check all bearish divergence columns
    bearish_columns = [
        'OBV_Regular_Bearish', 'VI_Regular_Bearish', 'Fisher_Regular_Bearish', 'Vol_Regular_Bearish',
        'OBV_Hidden_Bearish', 'VI_Hidden_Bearish', 'Fisher_Hidden_Bearish', 'Vol_Hidden_Bearish'
    ]
    
    # Get the index of the most recent bearish divergence
    for col in bearish_columns:
        if col in df.columns:
            last_divergence = df[df[col]].index[-1] if df[col].any() else None
            if last_divergence is not None:
                divergence_indices.append(last_divergence)
    
    if not divergence_indices:
        return pd.DataFrame()  # No divergence found
    
    # Get the most recent divergence (closest to current price)
    most_recent_divergence_idx = max(divergence_indices)
    divergence_row = df.loc[most_recent_divergence_idx]

    # 2. Check if any bullish divergence happened AFTER the bearish one
    bullish_columns = [
        'OBV_Regular_Bullish', 'VI_Regular_Bullish', 'Fisher_Regular_Bullish', 'Vol_Regular_Bullish',
        'OBV_Hidden_Bullish', 'VI_Hidden_Bullish', 'Fisher_Hidden_Bullish', 'Vol_Hidden_Bullish'
    ]
    
    newer_bullish = False
    for col in bullish_columns:
        if col in df.columns:
            # Check if a bullish signal appeared after the bearish divergence
            bullish_after = df.loc[most_recent_divergence_idx:][col].any()
            if bullish_after:
                newer_bullish = True
                break

    # 3. If confirmation is required, check price didn't invalidate the signal
    if require_confirmation:
        # Bearish divergence is invalidated if price makes a new high after
        post_divergence_df = df.loc[most_recent_divergence_idx:]
        if post_divergence_df['High'].max() > divergence_row['High']:
            return pd.DataFrame()  # Divergence invalidated

    # 4. Return the latest row if the most recent divergence was bearish and still valid
    if not newer_bullish:
        return df.iloc[-1:].copy()  # Return current candle
    
    return pd.DataFrame()  # Bullish divergence overrides

def calculate_indicator(df, **params):
    return scan_recent_bearish_divergence(df, **params)
