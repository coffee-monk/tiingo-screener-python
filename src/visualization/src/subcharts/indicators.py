import pandas as pd
import numpy as np
from src.visualization.src.color_palette import get_color_palette

colors = get_color_palette()


def add_visualizations(subchart, df):
    """
    Add visualization layers to subchart if input df column data is present
    """

    _FVG_visualization(subchart, df)
    _OB_visualization(subchart, df)
    _BoS_CHoCH_visualization(subchart, df)
    _liquidity_visualization(subchart, df)
    _banker_RSI_visualization(subchart, df)
    _aVWAP_visualization(subchart, df)
    _supertrend_visualization(subchart, df)
    _SMA_visualization(subchart, df)

    # Includes Regular/Hidden divergences for RSI, MACD, OBV, Volume, etc
    _combined_divergence_visualization(subchart, df)

def _FVG_visualization(subchart, df):
    if all(col in df.columns for col in ['FVG', 'FVG_High', 'FVG_Low', 'FVG_Mitigated_Index']):
        fvg_indices = df[df['FVG'] != 0].index
        for idx in fvg_indices:
            mit_idx = int(df.loc[idx, 'FVG_Mitigated_Index'])
            level = 'FVG_High' if df.loc[idx, 'FVG'] == 1 else 'FVG_Low'
            color = 'rgba(39,157,130,0.5)' if df.loc[idx, 'FVG'] == 1 else 'rgba(200,97,100,0.5)'
            end_date = (df.loc[mit_idx, 'date'] if 0 < mit_idx < len(df) 
                       else df.iloc[-1]['date'])
            subchart.create_line(
                price_line=False,
                price_label=False,
                color=color,
                width=2,
                style='dashed'
            ).set(pd.DataFrame({
                'date': [df.loc[idx, 'date'], end_date],
                'value': [df.loc[idx, level]] * 2
            }))


def _OB_visualization(subchart, df):
    if all(col in df.columns for col in ['OB', 'OB_High', 'OB_Low']):
        for idx in df[df['OB'] != 0].index:
            start_date = df.loc[idx, 'date']
            # Calculate midpoint between top and bottom
            midpoint = (df.loc[idx, 'OB_High'] + df.loc[idx, 'OB_Low']) / 2
            # Determine end date
            end_date = (df.loc[mitigation_idx, 'date'] if 'OB_Mitigated_Index' in df.columns 
                       and 0 < (mitigation_idx := int(df.loc[idx, 'OB_Mitigated_Index'])) < len(df)
                       else df.iloc[-1]['date'])
            # Draw single wider midpoint line
            subchart.create_line(
                price_line=False,
                price_label=False,
                color=colors['teal_OB'] if df.loc[idx, 'OB'] == 1 else colors['red_OB'],
                width=10,  # Wider line
                style='solid'
            ).set(pd.DataFrame({
                'date': [start_date, end_date],
                'value': [midpoint, midpoint]
            }))


def _BoS_CHoCH_visualization(subchart, df):
    if all(col in df.columns for col in ['BoS', 'CHoCH', 'BoS_CHoCH_Price', 'BoS_CHoCH_Break_Index']):
        # Get most recent 10 BoS/CHoCH events (combined)
        events = df[(df['BoS'] != 0) | (df['CHoCH'] != 0)].index[-25:]
        for idx in events:
            start_date = df.loc[idx, 'date']
            break_idx = int(df.loc[idx, 'BoS_CHoCH_Break_Index'])
            price = df.loc[idx, 'BoS_CHoCH_Price']
            
            # Determine end date
            end_date = df.loc[break_idx, 'date'] if 0 < break_idx < len(df) else df.iloc[-1, 'date']
                
            # Determine color and style based on event type and direction
            if df.loc[idx, 'BoS'] != 0:  # Break of Structure
                color = 'rgba(39,157,130,0.75)' if df.loc[idx, 'BoS'] > 0 else 'rgba(200,97,100,0.75)'
                style = 'solid'
                width = 1  # Thinner lines for BoS
            else:  # Change of Character
                color = 'rgba(39,157,130,0.75)' if df.loc[idx, 'CHoCH'] > 0 else 'rgba(200,97,100,0.75)'
                style = 'solid'  # Changed from dashed to solid for better visibility
                width = 1  # Thicker lines for CHoCH
            # Create the line
            subchart.create_line(
                price_line=False,
                price_label=False,
                color=color,
                width=width,
                style=style
            ).set(pd.DataFrame({
                'date': [start_date, end_date],
                'value': [price, price]
            }))


def _liquidity_visualization(subchart, df):
    if all(col in df.columns for col in ['Liquidity', 'Liquidity_Level']):
        # Get all liquidity events (both bullish and bearish)
        liquidity_events = df[df['Liquidity'] != 0]
        
        for idx in liquidity_events.index:
            level = df.loc[idx, 'Liquidity_Level']
            direction = df.loc[idx, 'Liquidity']
            
            # Create horizontal line spanning full chart
            subchart.create_line(
                price_line=False,
                price_label=False,
                color=colors['orange_liquidity'],
                width=1,
                style='solid'
            ).set(pd.DataFrame({
                'date': [df.iloc[0]['date'], df.iloc[-1]['date']],  # Full chart width
                'value': [level, level]  # Constant price level
            }))


def _banker_RSI_visualization(subchart, df):
    if 'banker_RSI' in df.columns:
        # Color configuration
        color_rules = [
            (0, 5, colors['teal_trans_3']),
            (5, 10, colors['teal']),
            (10, 15, colors['aqua']),
            (15, 20, colors['neon'])
        ]
        if 'volume' in df.columns:
            scale_margin_top = 0.85
            scale_margin_bottom = 0.1
        else: 
            scale_margin_top = 0.95
            scale_margin_bottom = 0.0
        # Create the histogram
        rsi_hist = subchart.create_histogram(
            color='rgba(100, 100, 100, 0.4)',  # Default neutral color
            price_line=False,
            price_label=False,
            scale_margin_top=scale_margin_top,
            scale_margin_bottom=scale_margin_bottom
        )
        # Prepare data with color column
        hist_data = pd.DataFrame({
            'time': df['date'],
            'value': df['banker_RSI'],
            'color': 'rgba(100, 100, 100, 0.4)'  # Initialize with default
        })
        # Apply color rules
        for low, high, color in color_rules:
            mask = (hist_data['value'] >= low) & (hist_data['value'] <= high)
            hist_data.loc[mask, 'color'] = color
        
        # Set the histogram data
        rsi_hist.set(hist_data)


def _aVWAP_visualization(subchart, df):
    # Plot peak aVWAPs (red)
    peak_cols = [col for col in df.columns if col.startswith('aVWAP_peak_')]
    for col in peak_cols:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['red_trans_3'],
            width=1
        ).set(df[['date', col]].rename(columns={col: 'value'}))
    
    # Plot valley aVWAPs (green)
    valley_cols = [col for col in df.columns if col.startswith('aVWAP_valley_')]
    for col in valley_cols:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['teal_trans_3'],
            width=1
        ).set(df[['date', col]].rename(columns={col: 'value'}))
    
    # Plot gap up aVWAPs (gray)
    gap_cols = [col for col in df.columns if col.startswith('Gap_Up_aVWAP_')]
    for col in gap_cols:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['teal_trans_2'],
            width=1,
            style='dotted'
        ).set(df[['date', col]].rename(columns={col: 'value'}))

    # Plot gap down aVWAPs (gray)
    gap_cols = [col for col in df.columns if col.startswith('Gap_Down_aVWAP_')]
    for col in gap_cols:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['red_trans_2'],
            width=1,
            style='dotted'
        ).set(df[['date', col]].rename(columns={col: 'value'}))

    # Order Blocks (OB) Bullish + Bearish

    OB_bull_cols = [col for col in df.columns if col.startswith('aVWAP_OB_bull_')]
    for col in OB_bull_cols:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['teal'],
            width=1
        ).set(df[['date', col]].rename(columns={col: 'value'}))

    OB_bear_cols = [col for col in df.columns if col.startswith('aVWAP_OB_bear_')]
    for col in OB_bear_cols:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['red'],
            width=1
        ).set(df[['date', col]].rename(columns={col: 'value'}))
    
    # Average aVWAPs (Gaps, Peaks/Valleys, OBs)

    if 'Peaks_Valleys_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['orange_aVWAP'],
            width=5
        ).set(df[['date', 'Peaks_Valleys_avg']].rename(columns={'Peaks_Valleys_avg': 'value'}))

    if 'OB_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['orange_aVWAP'],
            width=5
        ).set(df[['date', 'OB_avg']].rename(columns={'OB_avg': 'value'}))

    if 'Gaps_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['gray'],
            width=5
        ).set(df[['date', 'Gaps_avg']].rename(columns={'Gaps_avg': 'value'}))

    if 'All_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['orange_aVWAP'],
            width=5
        ).set(df[['date', 'All_avg']].rename(columns={'All_avg': 'value'}))


def _supertrend_visualization(subchart, df):
    if all(col in df.columns for col in ['Supertrend_Upper', 'Supertrend_Lower', 'Supertrend_Direction']):
        # Upper band (resistance in downtrend)
        upper_line = subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['orange'],
            width=1.0,
        )
        upper_line.set(df[['date', 'Supertrend_Upper']].rename(columns={'Supertrend_Upper': 'value'}))
        
        # Lower band (support in uptrend)
        lower_line = subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['orange'],
            width=1.0,
        )
        lower_line.set(df[['date', 'Supertrend_Lower']].rename(columns={'Supertrend_Lower': 'value'}))
        
        # Active band (solid line showing current trend)
        active_supertrend = np.where(
            df['Supertrend_Direction'] == -1,
            df['Supertrend_Lower'],
            df['Supertrend_Upper']
        )
        active_line = subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['black'],
            width=2.0  # Thicker to cover upper/lower bands for visualization
        )
        active_line.set(df[['date']].assign(value=active_supertrend))


def _SMA_visualization(subchart, df):
    sma_cols = [col for col in df.columns if col.startswith('SMA_')]
    for sma_col in sma_cols:
        # Extract period and determine width inline
        period = int(sma_col.split('_')[1]) if '_' in sma_col else 0
        subchart.create_line(
            price_line=False, 
            price_label=False,
            color=colors['blue_SMA'],
            width=( 1 if period <= 10 else
                    3 if period <= 50 else
                    5 if period <= 100 else
                    7 if period <= 200 else 9 )
        ).set(df[['date', sma_col]].rename(columns={sma_col: 'value'}))

# Divergences -----------------------------------------------------------------

def _rsi_divergence_visualization(subchart, df):
    """Visualizes all RSI divergences using explicit 'date' column"""
    required_cols = ['date', 'RSI_Regular_Bullish', 'RSI_Regular_Bearish',
                    'RSI_Hidden_Bullish', 'RSI_Hidden_Bearish']
    
    if not all(col in df.columns for col in required_cols):
        return

    # Initialize markers
    markers = []
    
    # Combine all bullish signals (regular + hidden)
    bull_mask = df['RSI_Regular_Bullish'] | df['RSI_Hidden_Bullish']
    for _, row in df[bull_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'below',
            'shape': 'square',
            'color': colors['teal'],
            'text': ''
        })
    
    # Combine all bearish signals (regular + hidden)
    bear_mask = df['RSI_Regular_Bearish'] | df['RSI_Hidden_Bearish']
    for _, row in df[bear_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'above',
            'shape': 'square',
            'color': colors['red'],
            'text': ''
        })
    
    # Add sorted markers
    if markers:
        subchart.marker_list(sorted(markers, key=lambda x: x['time']))


def _macd_divergence_visualization(subchart, df):
    """Visualizes MACD divergences with explicit date column"""
    required_cols = ['date', 'MACD_Regular_Bullish', 'MACD_Regular_Bearish',
                    'MACD_Hidden_Bullish', 'MACD_Hidden_Bearish']
    
    if not all(col in df.columns for col in required_cols):
        return
    
    # Initialize markers
    markers = []
    
    # Bullish signals (both regular and hidden)
    bull_mask = df['MACD_Regular_Bullish'] | df['MACD_Hidden_Bullish']
    for _, row in df[bull_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'below',
            'shape': 'square',
            'color': colors['teal'],
            'text': ''
        })
    
    # Bearish signals (both regular and hidden)
    bear_mask = df['MACD_Regular_Bearish'] | df['MACD_Hidden_Bearish']
    for _, row in df[bear_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'above',
            'shape': 'square',
            'color': colors['red'],
            'text': ''
        })
    
    # Add sorted markers
    if markers:
        subchart.marker_list(sorted(markers, key=lambda x: x['time']))


def _obv_divergence_visualization(subchart, df):
    """Visualizes OBV divergences with explicit date column"""
    required_cols = ['date', 'OBV_Regular_Bullish', 'OBV_Regular_Bearish',
                    'OBV_Hidden_Bullish', 'OBV_Hidden_Bearish']
    
    if not all(col in df.columns for col in required_cols):
        return
    
    # Initialize markers
    markers = []
    
    # Bullish signals (both regular and hidden)
    bull_mask = df['OBV_Regular_Bullish'] | df['OBV_Hidden_Bullish']
    for _, row in df[bull_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'below',
            'shape': 'square',
            'color': colors['teal'],  # Light green
            'text': ''
        })
    
    # Bearish signals (both regular and hidden)
    bear_mask = df['OBV_Regular_Bearish'] | df['OBV_Hidden_Bearish']
    for _, row in df[bear_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'above',
            'shape': 'square',
            'color': colors['red'],  # Light red
            'text': ''
        })
    
    # Add sorted markers
    if markers:
        subchart.marker_list(sorted(markers, key=lambda x: x['time']))


def _fischer_divergence_visualization(subchart, df):
    """Visualizes Fisher Transform divergences with purple/gold markers"""
    required_cols = ['date', 'Fisher_Regular_Bullish', 'Fisher_Regular_Bearish',
                    'Fisher_Hidden_Bullish', 'Fisher_Hidden_Bearish']
    
    if not all(col in df.columns for col in required_cols):
        return
    
    # Initialize markers
    markers = []
    
    # Bullish signals (both regular and hidden)
    bull_mask = df['Fisher_Regular_Bullish'] | df['Fisher_Hidden_Bullish']
    for _, row in df[bull_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'below',
            'shape': 'square',
            'color': colors['teal'],
            'text': ''
        })
    
    # Bearish signals (both regular and hidden)
    bear_mask = df['Fisher_Regular_Bearish'] | df['Fisher_Hidden_Bearish']
    for _, row in df[bear_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'above',
            'shape': 'square',
            'color': colors['red'],
            'text': ''
        })
    
    # Add sorted markers
    if markers:
        subchart.marker_list(sorted(markers, key=lambda x: x['time']))


def _vortex_divergence_visualization(subchart, df):
    """Visualizes Vortex divergences with explicit date column"""
    required_cols = ['date', 'VI_Regular_Bullish', 'VI_Regular_Bearish',
                    'VI_Hidden_Bullish', 'VI_Hidden_Bearish']
    
    if not all(col in df.columns for col in required_cols):
        return
    
    # Initialize markers
    markers = []
    
    # Bullish signals (both regular and hidden)
    bull_mask = df['VI_Regular_Bullish'] | df['VI_Hidden_Bullish']
    for _, row in df[bull_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'below',
            'shape': 'square',
            'color': colors['teal'],  # Consistent with OBV
            'text': ''
        })
    
    # Bearish signals (both regular and hidden)
    bear_mask = df['VI_Regular_Bearish'] | df['VI_Hidden_Bearish']
    for _, row in df[bear_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'above',
            'shape': 'square',
            'color': colors['red'],  # Consistent with OBV
            'text': ''
        })
    
    # Add sorted markers (critical for clean rendering)
    if markers:
        subchart.marker_list(sorted(markers, key=lambda x: x['time']))


def _momentum_divergence_visualization(subchart, df):
    """Visualizes Momentum divergences with explicit date column"""
    required_cols = ['date', 'Momo_Regular_Bullish', 'Momo_Regular_Bearish',
                    'Momo_Hidden_Bullish', 'Momo_Hidden_Bearish']
    
    if not all(col in df.columns for col in required_cols):
        return
    
    # Initialize markers
    markers = []
    
    # Bullish signals (both regular and hidden)
    bull_mask = df['Momo_Regular_Bullish'] | df['Momo_Hidden_Bullish']
    for _, row in df[bull_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'below',
            'shape': 'square',
            'color': colors['teal'],  # Matching OBV/Vortex style
            'text': ''
        })
    
    # Bearish signals (both regular and hidden)
    bear_mask = df['Momo_Regular_Bearish'] | df['Momo_Hidden_Bearish']
    for _, row in df[bear_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'above',
            'shape': 'square',
            'color': colors['red'],  # Matching OBV/Vortex style
            'text': ''
        })
    
    # Add sorted markers to prevent rendering artifacts
    if markers:
        subchart.marker_list(sorted(markers, key=lambda x: x['time']))


def _volume_divergence_visualization(subchart, df):
    """Visualizes volume divergences using square markers"""
    required_cols = ['date', 'Vol_Regular_Bullish', 'Vol_Regular_Bearish',
                    'Vol_Hidden_Bullish', 'Vol_Hidden_Bearish']
    
    if not all(col in df.columns for col in required_cols):
        return
    
    markers = []
    
    # Bullish signals - blue squares below price
    bull_mask = df['Vol_Regular_Bullish'] | df['Vol_Hidden_Bullish']
    for _, row in df[bull_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'below',
            'shape': 'square',
            'color': colors['teal'],            
            'text': ''
        })
    
    # Bearish signals - orange squares above price
    bear_mask = df['Vol_Regular_Bearish'] | df['Vol_Hidden_Bearish']
    for _, row in df[bear_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'above',
            'shape': 'square',
            'color': colors['red'],            
            'text': ''
        })
    
    if markers:
        subchart.marker_list(sorted(markers, key=lambda x: x['time']))


def _atr_divergence_visualization(subchart, df):
    """Visualizes ATR divergences with diamond markers"""
    required_cols = ['date', 'ATR_Regular_Bullish', 'ATR_Regular_Bearish',
                    'ATR_Hidden_Bullish', 'ATR_Hidden_Bearish']
    
    if not all(col in df.columns for col in required_cols):
        return
    
    markers = []
    
    # Bullish signals (both regular and hidden)
    bull_mask = df['ATR_Regular_Bullish'] | df['ATR_Hidden_Bullish']
    for _, row in df[bull_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'below',
            'shape': 'square',
            'color': colors['teal'],
            'text': ''
        })
    
    # Bearish signals (both regular and hidden)
    bear_mask = df['ATR_Regular_Bearish'] | df['ATR_Hidden_Bearish']
    for _, row in df[bear_mask].iterrows():
        markers.append({
            'time': row['date'],
            'position': 'above',
            'shape': 'square',
            'color': colors['red'],
            'text': ''
        })
    
    # Add sorted markers
    if markers:
        subchart.marker_list(sorted(markers, key=lambda x: x['time']))




def _combined_divergence_visualization(subchart, df):
    """Combined visualization for all divergence types in one marker pass"""
    # Define all divergence types with their config
    divergence_types = [
        {
            'name': 'RSI',
            'bull_cols': ['RSI_Regular_Bullish', 'RSI_Hidden_Bullish'],
            'bear_cols': ['RSI_Regular_Bearish', 'RSI_Hidden_Bearish'],
            'bull_shape': 'square', # arrow_up
            'bear_shape': 'square', # arrow_down
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'MACD',
            'bull_cols': ['MACD_Regular_Bullish', 'MACD_Hidden_Bullish'],
            'bear_cols': ['MACD_Regular_Bearish', 'MACD_Hidden_Bearish'],
            'bull_shape': 'square',
            'bear_shape': 'square',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'OBV',
            'bull_cols': ['OBV_Regular_Bullish', 'OBV_Hidden_Bullish'],
            'bear_cols': ['OBV_Regular_Bearish', 'OBV_Hidden_Bearish'],
            'bull_shape': 'square',
            'bear_shape': 'square',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'Fisher',
            'bull_cols': ['Fisher_Regular_Bullish', 'Fisher_Hidden_Bullish'],
            'bear_cols': ['Fisher_Regular_Bearish', 'Fisher_Hidden_Bearish'],
            'bull_shape': 'square',
            'bear_shape': 'square',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'Vortex',
            'bull_cols': ['VI_Regular_Bullish', 'VI_Hidden_Bullish'],
            'bear_cols': ['VI_Regular_Bearish', 'VI_Hidden_Bearish'],
            'bull_shape': 'square',
            'bear_shape': 'square',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'Momentum',
            'bull_cols': ['Momo_Regular_Bullish', 'Momo_Hidden_Bullish'],
            'bear_cols': ['Momo_Regular_Bearish', 'Momo_Hidden_Bearish'],
            'bull_shape': 'square',
            'bear_shape': 'square',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'Volume',
            'bull_cols': ['Vol_Regular_Bullish', 'Vol_Hidden_Bullish'],
            'bear_cols': ['Vol_Regular_Bearish', 'Vol_Hidden_Bearish'],
            'bull_shape': 'square',
            'bear_shape': 'square',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'ATR',
            'bull_cols': ['ATR_Regular_Bullish', 'ATR_Hidden_Bullish'],
            'bear_cols': ['ATR_Regular_Bearish', 'ATR_Hidden_Bearish'],
            'bull_shape': 'square',
            'bear_shape': 'square',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        }
    ]

    markers = []
    
    for div in divergence_types:
        # Check if required columns exist
        required_cols = div['bull_cols'] + div['bear_cols'] + ['date']
        if not all(col in df.columns for col in required_cols):
            continue
        
        # Process bullish signals
        bull_mask = df[div['bull_cols']].any(axis=1)
        for _, row in df[bull_mask].iterrows():
            markers.append({
                'time': row['date'],
                'position': 'below',
                'shape': div['bull_shape'],
                'color': div['bull_color'],
                'text': ''
            })
        
        # Process bearish signals
        bear_mask = df[div['bear_cols']].any(axis=1)
        for _, row in df[bear_mask].iterrows():
            markers.append({
                'time': row['date'],
                'position': 'above',
                'shape': div['bear_shape'],
                'color': div['bear_color'],
                'text': ''
            })
    
    # Add all markers in one pass (sorted chronologically)
    if markers:
        subchart.marker_list(sorted(markers, key=lambda x: x['time']))
