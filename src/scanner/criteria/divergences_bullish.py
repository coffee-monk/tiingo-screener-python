import pandas as pd

def divergences_bullish(
    df: pd.DataFrame,
    max_bars_back: int = 20,  # How far back to check for divergences
    require_confirmation: bool = True,  # Wait for 1-2 bars of confirmation
) -> pd.DataFrame:
    """
    Scan for the most recent bullish divergence (if any) and check if it's still valid.
    
    Returns:
        - Latest row if the most recent divergence was bullish and still active.
        - Empty DataFrame otherwise.
    """
    if len(df) < 2:
        return pd.DataFrame()

    # 1. Find the most recent bullish divergence (regular or hidden)
    divergence_indices = []
    
    # Check all bullish divergence columns
    bullish_columns = [
        'OBV_Regular_Bullish', 'VI_Regular_Bullish', 'Fisher_Regular_Bullish', 'Vol_Regular_Bullish',
        'OBV_Hidden_Bullish', 'VI_Hidden_Bullish', 'Fisher_Hidden_Bullish', 'Vol_Hidden_Bullish'
    ]
    
    # Get the index of the most recent bullish divergence
    for col in bullish_columns:
        if col in df.columns:
            last_divergence = df[df[col]].index[-1] if df[col].any() else None
            if last_divergence is not None:
                divergence_indices.append(last_divergence)
    
    if not divergence_indices:
        return pd.DataFrame()  # No divergence found
    
    # Get the most recent divergence (closest to current price)
    most_recent_divergence_idx = max(divergence_indices)
    divergence_row = df.loc[most_recent_divergence_idx]

    # 2. Check if any bearish divergence happened AFTER the bullish one
    bearish_columns = [
        'OBV_Regular_Bearish', 'VI_Regular_Bearish', 'Fisher_Regular_Bearish', 'Vol_Regular_Bearish',
        'OBV_Hidden_Bearish', 'VI_Hidden_Bearish', 'Fisher_Hidden_Bearish', 'Vol_Hidden_Bearish'
    ]
    
    newer_bearish = False
    for col in bearish_columns:
        if col in df.columns:
            # Check if a bearish signal appeared after the bullish divergence
            bearish_after = df.loc[most_recent_divergence_idx:][col].any()
            if bearish_after:
                newer_bearish = True
                break

    # 3. If confirmation is required, check price didn't invalidate the signal
    if require_confirmation:
        # Bullish divergence is invalidated if price makes a new low after
        post_divergence_df = df.loc[most_recent_divergence_idx:]
        if post_divergence_df['Low'].min() < divergence_row['Low']:
            return pd.DataFrame()  # Divergence invalidated

    # 4. Return the latest row if the most recent divergence was bullish and still valid
    if not newer_bearish:
        return df.iloc[-1:].copy()  # Return current candle
    
    return pd.DataFrame()  # Bearish divergence overrides

def calculate_indicator(df, **params):
    return scan_recent_bullish_divergence(df, **params)
