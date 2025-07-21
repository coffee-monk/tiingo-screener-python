import pandas as pd
from typing import Literal, Optional

def OB_aVWAP(
    df: pd.DataFrame,
    mode: Literal['bullish', 'bearish'] = 'bullish',
    distance_pct: float = 1.0,
    direction: Literal['below', 'above', 'within'] = 'within',
    require_in_range: bool = False,
    max_lookback: Optional[int] = None
) -> pd.DataFrame:
    """
    Unified scanner for price relative to Order Block's anchored VWAP.
    
    Parameters:
        df: DataFrame containing:
            - 'OB' (1=bullish, -1=bearish, 0=neutral)
            - 'OB_High', 'OB_Low' (price range)
            - 'Close' (current price)
            - Columns matching pattern: 'aVWAP_OB_bull_*' or 'aVWAP_OB_bear_*'
            
        mode: 'bullish' or 'bearish' - which OB type to scan for
        distance_pct: Percentage distance threshold from aVWAP
        direction: Price position relative to aVWAP:
            - 'below': Price below OB's aVWAP
            - 'above': Price above OB's aVWAP
            - 'within': Price near aVWAP (either side)
        require_in_range: If True, price must also be within OB's High/Low range
        max_lookback: Max bars to look back for OBs (None for all history)
            
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty
    """
    if len(df) == 0:
        return pd.DataFrame()

    latest = df.iloc[-1]
    target_ob = 1 if mode == 'bullish' else -1
    avwap_prefix = f'aVWAP_OB_bull_' if mode == 'bullish' else f'aVWAP_OB_bear_'

    # Apply lookback window if specified
    scan_range = df
    if max_lookback is not None:
        scan_range = df.iloc[-max_lookback:]

    # Find most recent OB of specified type
    for i in range(len(scan_range)-1, -1, -1):
        if scan_range['OB'].iloc[i] == target_ob:
            ob_high = scan_range['OB_High'].iloc[i]
            ob_low = scan_range['OB_Low'].iloc[i]
            avwap_col = f'{avwap_prefix}{i}'
            
            if avwap_col in df.columns and pd.notna(df[avwap_col].iloc[-1]):
                current_avwap = df[avwap_col].iloc[-1]
                distance = (latest['Close'] - current_avwap) / current_avwap * 100
                
                # Check if price is within OB range (if required)
                in_range = True
                if require_in_range:
                    in_range = (latest['Close'] >= ob_low) and (latest['Close'] <= ob_high)
                
                # Direction conditions
                if direction == 'below':
                    condition = (-distance_pct <= distance <= 0)
                elif direction == 'above':
                    condition = (0 <= distance <= distance_pct)
                else:  # 'within'
                    condition = abs(distance) <= distance_pct
                
                if condition and in_range:
                    return pd.DataFrame({
                        'Close': latest['Close'],
                        'Signal': f'{mode.capitalize()}OB_aVWAP_{direction}',
                        'OB_aVWAP': current_avwap,
                        'OB_High': ob_high,
                        'OB_Low': ob_low,
                        'Distance_Pct': distance,
                        'Position': 'below' if distance < 0 else 'above',
                        'OB_Index': i,
                        'OB_Mode': mode
                    }, index=[latest.name])
            
            break  # Only check most recent OB
    
    return pd.DataFrame()

def calculate_indicator(df, **params):
    """Standard interface wrapper"""
    return OB_aVWAP(df, **params)
