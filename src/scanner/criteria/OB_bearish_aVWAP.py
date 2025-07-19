import pandas as pd

def OB_bearish_aVWAP(df, distance_pct=1.0, direction='within'):
    """
    Scan for price relative to bearish Order Block's aVWAP with distance control.
    
    Parameters:
        df (pd.DataFrame): Must contain:
            - 'OB' (1=bullish, -1=bearish, 0=neutral)
            - 'OB_High', 'OB_Low' (price range of OB)
            - 'Close' (current price)
            - Columns matching 'aVWAP_OB_bear_*' pattern
        distance_pct: Percentage distance threshold from aVWAP
        direction: Where to look relative to OB's aVWAP:
                  'below' - Price below OB's aVWAP
                  'above' - Price above OB's aVWAP  
                  'within' - Price near OB's aVWAP (either side)
    
    Returns:
        pd.DataFrame: Signal details if conditions met, else empty.
    """
    latest = df.iloc[-1]
    
    # Find most recent bearish OB
    for i in range(len(df)-1, -1, -1):
        if df['OB'].iloc[i] == -1:  # -1 indicates bearish OB
            ob_high = df['OB_High'].iloc[i]
            ob_low = df['OB_Low'].iloc[i]
            avwap_col = f'aVWAP_OB_bear_{i}'
            
            if avwap_col in df.columns and pd.notna(df[avwap_col].iloc[-1]):
                current_avwap = df[avwap_col].iloc[-1]
                distance = (latest['Close'] - current_avwap) / current_avwap * 100
                
                # Check if price is within OB range (optional)
                price_in_ob_range = (latest['Close'] >= ob_low) and (latest['Close'] <= ob_high)
                
                # Directional conditions
                if direction == 'below':
                    condition = (-distance_pct <= distance <= 0)  # Price below aVWAP
                elif direction == 'above':
                    condition = (0 <= distance <= distance_pct)   # Price above aVWAP
                else:  # 'within'
                    condition = abs(distance) <= distance_pct     # Price near aVWAP
                
                if condition:
                    return pd.DataFrame({
                        'Close': latest['Close'],
                        'Signal': f'BearOB_aVWAP_{direction}',
                        'OB_aVWAP': current_avwap,
                        'OB_High': ob_high,
                        'OB_Low': ob_low,
                        'Distance_Pct': distance,
                        'Position': 'below' if distance < 0 else 'above',
                        'OB_Index': i  # Location of the OB in dataframe
                    }, index=[latest.name])
            
            break  # Only check most recent OB
    
    return pd.DataFrame()
