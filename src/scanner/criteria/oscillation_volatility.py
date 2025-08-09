import pandas as pd
from typing import Optional

def oscillation_volatility(
    df: pd.DataFrame,
    cross_count: Optional[int] = None,
    cross_count_max: Optional[int] = None,
    avg_deviation: Optional[float] = None,
    avg_deviation_max: Optional[float] = None,
    oscillation_score: Optional[float] = None,
    oscillation_score_max: Optional[float] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Enhanced oscillation volatility scanner with explicit min/max controls.
    
    Parameters:
        cross_count: Minimum MA crosses required (None means no minimum)
        cross_count_max: Maximum MA crosses allowed (None means no maximum)
        avg_deviation: Minimum std dev from MA required
        avg_deviation_max: Maximum std dev from MA allowed
        oscillation_score: Minimum score (count*deviation) required
        oscillation_score_max: Maximum score (count*deviation) allowed
    
    Returns:
        pd.DataFrame: Single-row DataFrame if conditions met, else empty.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    # Check required columns exist
    required_cols = ['MA_Cross_Count', 'MA_Avg_Deviation_Z', 'MA_Oscillation_Score']
    if not all(col in df.columns for col in required_cols):
        return pd.DataFrame()
    
    latest = df.iloc[-1]
    
    # Check cross count conditions
    cross_ok = True
    if cross_count is not None:
        cross_ok &= (latest['MA_Cross_Count'] >= cross_count)
    if cross_count_max is not None:
        cross_ok &= (latest['MA_Cross_Count'] <= cross_count_max)
    
    # Check deviation conditions
    dev_ok = True
    if avg_deviation is not None:
        dev_ok &= (latest['MA_Avg_Deviation_Z'] >= avg_deviation)
    if avg_deviation_max is not None:
        dev_ok &= (latest['MA_Avg_Deviation_Z'] <= avg_deviation_max)
    
    # Check score conditions
    score_ok = True
    if oscillation_score is not None:
        score_ok &= (latest['MA_Oscillation_Score'] >= oscillation_score)
    if oscillation_score_max is not None:
        score_ok &= (latest['MA_Oscillation_Score'] <= oscillation_score_max)
    
    return df.iloc[-1:].copy() if (cross_ok and dev_ok and score_ok) else pd.DataFrame()

def calculate_indicator(df, **params):
    """Wrapper for consistent interface"""
    return oscillation_volatility(df, **params)
