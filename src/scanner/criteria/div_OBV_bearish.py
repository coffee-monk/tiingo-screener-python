import pandas as pd

def div_OBV_bearish(
    df: pd.DataFrame,
    max_bars_back: int = 20,
    require_confirmation: bool = True,
) -> pd.DataFrame:
    """Same logic but for OBV bearish divergences"""
    if len(df) < 2:
        return pd.DataFrame()

    divergence_indices = []
    obv_bearish_columns = ['OBV_Regular_Bearish', 'OBV_Hidden_Bearish']
    
    for col in obv_bearish_columns:
        if col in df.columns:
            last_divergence = df[df[col]].index[-1] if df[col].any() else None
            if last_divergence is not None:
                divergence_indices.append(last_divergence)
    
    if not divergence_indices:
        return pd.DataFrame()
    
    most_recent_divergence_idx = max(divergence_indices)
    divergence_row = df.loc[most_recent_divergence_idx]

    obv_bullish_columns = ['OBV_Regular_Bullish', 'OBV_Hidden_Bullish']
    newer_bullish = False
    for col in obv_bullish_columns:
        if col in df.columns:
            if df.loc[most_recent_divergence_idx:][col].any():
                newer_bullish = True
                break

    if require_confirmation:
        if df.loc[most_recent_divergence_idx:]['High'].max() > divergence_row['High']:
            return pd.DataFrame()

    if not newer_bullish:
        return df.iloc[-1:].copy()
    
    return pd.DataFrame()

def calculate_indicator(df, **params):
    return div_OBV_bearish(df, **params)
