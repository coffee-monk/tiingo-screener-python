import pandas as pd
from typing import List, Optional

def divergences(
    df: pd.DataFrame,
    divergence_types: Optional[List[str]] = None,
    mode: str = 'bearish',
    max_bars_back: int = 20,
    require_confirmation: bool = True
) -> pd.DataFrame:
    """
    Scan for the most recent divergence (bearish or bullish) and check if it's still valid.
    
    Parameters:
        df: Input DataFrame with price and indicator data
        divergence_types: List of divergence types to check 
            (e.g., ['OBV', 'VI', 'Fisher', 'Vol'] or None for all)
        mode: 'bearish' or 'bullish' - which type of divergence to scan for
        max_bars_back: Only consider divergences within last N bars (None for all history)
        require_confirmation: Whether to require price confirmation
        
    Returns:
        Latest row if valid divergence found, else empty DataFrame
    """
    if len(df) < 2:
        return pd.DataFrame()

    # Set default divergence types if not specified
    if divergence_types is None:
        divergence_types = ['OBV', 'VI', 'Fisher', 'Vol']
    
    # Validate mode
    mode = mode.lower()
    if mode not in ['bearish', 'bullish']:
        raise ValueError("mode must be either 'bearish' or 'bullish'")

    # 1. Determine which columns to check based on divergence_types and mode
    target_columns = []
    opposite_columns = []
    
    for div_type in divergence_types:
        # Columns for the mode we're interested in
        target_columns.extend([
            f'{div_type}_Regular_{mode.capitalize()}',
            f'{div_type}_Hidden_{mode.capitalize()}'
        ])
        
        # Columns for the opposite mode (to check for invalidations)
        opposite_mode = 'bullish' if mode == 'bearish' else 'bearish'
        opposite_columns.extend([
            f'{div_type}_Regular_{opposite_mode.capitalize()}',
            f'{div_type}_Hidden_{opposite_mode.capitalize()}'
        ])
    
    # 2. Find all candidate divergences
    divergence_indices = []
    
    for col in target_columns:
        if col in df.columns:
            # Get indices where this divergence type occurred
            div_indices = df[df[col]].index.tolist()
            divergence_indices.extend(div_indices)
    
    # 3. Apply max_bars_back filter if specified
    if max_bars_back is not None and len(df) > max_bars_back:
        if isinstance(df.index, pd.DatetimeIndex):
            # For datetime indices, use timestamp comparison
            cutoff = df.index[-max_bars_back - 1]
            divergence_indices = [idx for idx in divergence_indices if idx >= cutoff]
        else:
            # For integer indices, use position comparison
            min_pos = len(df) - max_bars_back
            divergence_indices = [idx for idx in divergence_indices 
                                if df.index.get_loc(idx) >= min_pos]
    
    if not divergence_indices:
        return pd.DataFrame()  # No divergence found in lookback window
    
    # 4. Get the most recent divergence
    most_recent_divergence_idx = max(divergence_indices)
    divergence_row = df.loc[most_recent_divergence_idx]

    # 5. Check if any opposite divergence happened AFTER our signal
    newer_opposite = False
    for col in opposite_columns:
        if col in df.columns:
            opposite_after = df.loc[most_recent_divergence_idx:][col].any()
            if opposite_after:
                newer_opposite = True
                break

    # 6. If confirmation is required, check price didn't invalidate the signal
    if require_confirmation:
        if mode == 'bearish':
            # Bearish divergence invalidated if price makes new high
            post_divergence_max = df.loc[most_recent_divergence_idx:]['High'].max()
            if post_divergence_max > divergence_row['High']:
                return pd.DataFrame()
        else:
            # Bullish divergence invalidated if price makes new low
            post_divergence_min = df.loc[most_recent_divergence_idx:]['Low'].min()
            if post_divergence_min < divergence_row['Low']:
                return pd.DataFrame()

    # 7. Return the latest row if the divergence is still valid
    if not newer_opposite:
        return df.iloc[-1:].copy()
    
    return pd.DataFrame()

def calculate_indicator(df, **params):
    return divergences(df, **params)
