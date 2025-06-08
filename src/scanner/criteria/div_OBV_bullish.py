import pandas as pd

def div_OBV_bullish(
    df: pd.DataFrame,
    max_bars_back: int = 20,  # How far back to check for divergences
    require_confirmation: bool = True,  # Wait for 1-2 bars of confirmation
) -> pd.DataFrame:
    """
    Scan for the most recent OBV bullish divergence (regular or hidden) and check if it's still valid.
    
    Returns:
        - Latest row if the most recent OBV divergence was bullish and still active.
        - Empty DataFrame otherwise.
    """
    if len(df) < 2:
        return pd.DataFrame()

    # 1. Find the most recent OBV bullish divergence
    divergence_indices = []
    
    # Check only OBV divergence columns
    obv_bullish_columns = [
        'OBV_Regular_Bullish', 
        'OBV_Hidden_Bullish'
    ]
    
    # Get the index of the most recent OBV bullish divergence
    for col in obv_bullish_columns:
        if col in df.columns:
            last_divergence = df[df[col]].index[-1] if df[col].any() else None
            if last_divergence is not None:
                divergence_indices.append(last_divergence)
    
    if not divergence_indices:
        return pd.DataFrame()  # No OBV divergence found
    
    # Get the most recent OBV divergence
    most_recent_divergence_idx = max(divergence_indices)
    divergence_row = df.loc[most_recent_divergence_idx]

    # 2. Check if any OBV bearish divergence happened AFTER the bullish one
    obv_bearish_columns = [
        'OBV_Regular_Bearish',
        'OBV_Hidden_Bearish'
    ]
    
    newer_bearish = False
    for col in obv_bearish_columns:
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

    # 4. Return the latest row if the most recent OBV divergence was bullish and still valid
    if not newer_bearish:
        return df.iloc[-1:].copy()  # Return current candle
    
    return pd.DataFrame()  # Bearish divergence overrides

def calculate_indicator(df, **params):
    return div_OBV_bullish(df, **params)
