import pandas as pd
import numpy as np
from src.visualization.src.color_palette import get_color_palette

colors = get_color_palette()


def add_visualizations(subchart, df, show_banker_RSI):
    """
    Add visualization layers to subchart if input df column data is present
    """

    _FVG_visualization(subchart, df)
    _OB_visualization(subchart, df)
    _BoS_CHoCH_visualization(subchart, df)
    _liquidity_visualization(subchart, df)
    _aVWAP_visualization(subchart, df)
    _supertrend_visualization(subchart, df)
    _SMA_visualization(subchart, df)
    if show_banker_RSI: _banker_RSI_visualization(subchart, df)

    # Includes Regular/Hidden divergences for RSI, MACD, OBV, Volume, etc
    _combined_divergence_visualization(subchart, df)


def _FVG_visualization(subchart, df):
    if all(col in df.columns for col in ['FVG', 'FVG_High', 'FVG_Low', 'FVG_Mitigated_Index']):
        # Find the last row with actual data (before NaN padding)
        last_data_idx = df[['close', 'high', 'low', 'open']].last_valid_index()
        
        # Get all FVG occurrences (bullish=1, bearish=-1)
        fvg_indices = df[df['FVG'] != 0].index
        
        for idx in fvg_indices:
            # Get mitigation index (may be NaN, 0, or positive number)
            mit_idx = df.loc[idx, 'FVG_Mitigated_Index']
            
            # Determine if FVG is mitigated
            if pd.isna(mit_idx) or mit_idx == 0:
                # Unmitigated - draw only to last actual data point, not through padding
                end_idx = last_data_idx
            else:
                # Mitigated - convert to integer index
                end_idx = int(mit_idx)
                # Ensure it's within bounds of actual data
                end_idx = min(end_idx, last_data_idx)
            
            # Set visualization parameters
            fvg_type = df.loc[idx, 'FVG']
            level = 'FVG_High' if fvg_type == 1 else 'FVG_Low'
            color = colors['teal_trans_3'] if fvg_type == 1 else colors['red_trans_3']

            # Only create line if we have valid points to draw
            if idx <= end_idx:
                # Create the line
                subchart.create_line(
                    price_line=False,
                    price_label=False,
                    color=color,
                    width=1,
                    style='dashed'
                ).set(pd.DataFrame({
                    'date': [df.loc[idx, 'date'], df.loc[end_idx, 'date']],
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
    required_cols = ['BoS', 'CHoCH', 'BoS_CHoCH_Price', 'BoS_CHoCH_Break_Index']
    
    # First verify all required columns exist
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return
    
    # Now safely process the data
    df = df.dropna(subset=required_cols)
    events = df[(df['BoS'] != 0) | (df['CHoCH'] != 0)].index[-25:]
        
    for idx in events:
        start_date = df.loc[idx, 'date']
        price = df.loc[idx, 'BoS_CHoCH_Price']
        
        # Safely handle break index (NaN, None, or invalid values)
        try:
            break_idx = int(df.loc[idx, 'BoS_CHoCH_Break_Index'])
            # Ensure break index is within valid range
            if 0 < break_idx < len(df):
                end_date = df.loc[break_idx, 'date']
            else:
                end_date = df.iloc[-1]['date']
        except (ValueError, TypeError):
            end_date = df.iloc[-1]['date']  # Use last date if conversion fails
        
        # Determine color and style
        if df.loc[idx, 'BoS'] != 0:  # Break of Structure
            color = colors['teal_trans_3'] if df.loc[idx, 'BoS'] > 0 else colors['red_trans_3']
            style = 'solid'
            width = 1
        else:  # Change of Character
            color = colors['aqua'] if df.loc[idx, 'CHoCH'] > 0 else colors['red_dark']
            style = 'solid'
            width = 1
        
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

    # Plot gaps UP aVWAPs
    gap_cols = [col for col in df.columns if col.startswith('Gap_Up_aVWAP_')]
    for col in gap_cols:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['teal_trans_2'],
            width=1,
            style='dotted'
        ).set(df[['date', col]].rename(columns={col: 'value'}))

    # Plot gaps DOWN aVWAPs
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
            color=colors['aqua'],
            width=1
        ).set(df[['date', col]].rename(columns={col: 'value'}))

    OB_bear_cols = [col for col in df.columns if col.startswith('aVWAP_OB_bear_')]
    for col in OB_bear_cols:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['red_dark'],
            width=1
        ).set(df[['date', col]].rename(columns={col: 'value'}))

    BoS_CHoCH_bear_cols = [col for col in df.columns if col.startswith('aVWAP_BoS_CHoCH_bear_')]
    for col in BoS_CHoCH_bear_cols:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['red'],
            width=1
        ).set(df[['date', col]].rename(columns={col: 'value'}))

    BoS_CHoCH_bull_cols = [col for col in df.columns if col.startswith('aVWAP_BoS_CHoCH_bull_')]
    for col in BoS_CHoCH_bull_cols:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['teal'],
            width=1
        ).set(df[['date', col]].rename(columns={col: 'value'}))
    
    # Average aVWAPs (Gaps, Peaks/Valleys, OBs)

    if 'Peaks_Valleys_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['orange_aVWAP'],
            width=4
        ).set(df[['date', 'Peaks_Valleys_avg']].rename(columns={'Peaks_Valleys_avg': 'value'}))

    if 'Peaks_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['red'],
            width=4
        ).set(df[['date', 'Peaks_avg']].rename(columns={'Peaks_avg': 'value'}))

    if 'Valleys_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['teal'],
            width=4
        ).set(df[['date', 'Valleys_avg']].rename(columns={'Valleys_avg': 'value'}))

    if 'OB_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['orange_aVWAP'],
            width=3,
            style='dashed',
        ).set(df[['date', 'OB_avg']].rename(columns={'OB_avg': 'value'}))

    if 'Gaps_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['orange_aVWAP'],
            width=4,
            style='dotted',
        ).set(df[['date', 'Gaps_avg']].rename(columns={'Gaps_avg': 'value'}))

    if 'BoS_CHoCH_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['orange_aVWAP'],
            width=3,
            style='large_dashed',
        ).set(df[['date', 'BoS_CHoCH_avg']].rename(columns={'BoS_CHoCH_avg': 'value'}))

    if 'All_avg' in df.columns:
        subchart.create_line(
            price_line=False,
            price_label=False,
            color=colors['gray_trans'],
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


def _combined_divergence_visualization(subchart, df):
    """Combined visualization for all divergence types with shape differentiation"""
    # Define all divergence types with their config
    divergence_types = [
        {
            'name': 'RSI',
            'regular_bull_col': 'RSI_Regular_Bullish',
            'hidden_bull_col': 'RSI_Hidden_Bullish',
            'regular_bear_col': 'RSI_Regular_Bearish',
            'hidden_bear_col': 'RSI_Hidden_Bearish',
            'regular_shape': 'square',
            'hidden_shape': 'circle',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'Stochastic',
            'regular_bull_col': 'Stochastic_Regular_Bullish',
            'hidden_bull_col': 'Stochastic_Hidden_Bullish',
            'regular_bear_col': 'Stochastic_Regular_Bearish',
            'hidden_bear_col': 'Stochastic_Hidden_Bearish',
            'regular_shape': 'square',
            'hidden_shape': 'circle',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'MFI',
            'regular_bull_col': 'MFI_Regular_Bullish',
            'hidden_bull_col': 'MFI_Hidden_Bullish',
            'regular_bear_col': 'MFI_Regular_Bearish',
            'hidden_bear_col': 'MFI_Hidden_Bearish',
            'regular_shape': 'square',
            'hidden_shape': 'circle',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'Fractal',
            'regular_bull_col': 'Fractal_Bullish',
            'regular_bear_col': 'Fractal_Bearish',
            'regular_shape': 'square',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'MACD',
            'regular_bull_col': 'MACD_Regular_Bullish',
            'hidden_bull_col': 'MACD_Hidden_Bullish',
            'regular_bear_col': 'MACD_Regular_Bearish',
            'hidden_bear_col': 'MACD_Hidden_Bearish',
            'regular_shape': 'square',
            'hidden_shape': 'circle',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'OBV',
            'regular_bull_col': 'OBV_Regular_Bullish',
            'hidden_bull_col': 'OBV_Hidden_Bullish',
            'regular_bear_col': 'OBV_Regular_Bearish',
            'hidden_bear_col': 'OBV_Hidden_Bearish',
            'regular_shape': 'square',
            'hidden_shape': 'circle',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'Fisher',
            'regular_bull_col': 'Fisher_Regular_Bullish',
            'hidden_bull_col': 'Fisher_Hidden_Bullish',
            'regular_bear_col': 'Fisher_Regular_Bearish',
            'hidden_bear_col': 'Fisher_Hidden_Bearish',
            'regular_shape': 'square',
            'hidden_shape': 'circle',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'Vortex',
            'regular_bull_col': 'VI_Regular_Bullish',
            'hidden_bull_col': 'VI_Hidden_Bullish',
            'regular_bear_col': 'VI_Regular_Bearish',
            'hidden_bear_col': 'VI_Hidden_Bearish',
            'regular_shape': 'square',
            'hidden_shape': 'circle',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'Momentum',
            'regular_bull_col': 'Momo_Regular_Bullish',
            'hidden_bull_col': 'Momo_Hidden_Bullish',
            'regular_bear_col': 'Momo_Regular_Bearish',
            'hidden_bear_col': 'Momo_Hidden_Bearish',
            'regular_shape': 'square',
            'hidden_shape': 'circle',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'Volume',
            'regular_bull_col': 'Vol_Regular_Bullish',
            'hidden_bull_col': 'Vol_Hidden_Bullish',
            'regular_bear_col': 'Vol_Regular_Bearish',
            'hidden_bear_col': 'Vol_Hidden_Bearish',
            'regular_shape': 'square',
            'hidden_shape': 'circle',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        },
        {
            'name': 'ATR',
            'regular_bull_col': 'ATR_Regular_Bullish',
            'hidden_bull_col': 'ATR_Hidden_Bullish',
            'regular_bear_col': 'ATR_Regular_Bearish',
            'hidden_bear_col': 'ATR_Hidden_Bearish',
            'regular_shape': 'square',
            'hidden_shape': 'circle',
            'bull_color': colors['teal'],
            'bear_color': colors['red']
        }
    ]

    markers = []
    
    for div in divergence_types:
        # Process regular bullish signals
        if 'regular_bull_col' in div and div['regular_bull_col'] in df.columns:
            reg_bull_mask = df[div['regular_bull_col']].fillna(False).astype(bool)
            for _, row in df[reg_bull_mask].iterrows():
                markers.append({
                    'time': row['date'],
                    'position': 'below',
                    'shape': div['regular_shape'],
                    'color': div['bull_color'],
                    'text': ''
                })
        
        # Process hidden bullish signals
        if 'hidden_bull_col' in div and div['hidden_bull_col'] in df.columns:
            hid_bull_mask = df[div['hidden_bull_col']].fillna(False).astype(bool)
            for _, row in df[hid_bull_mask].iterrows():
                markers.append({
                    'time': row['date'],
                    'position': 'below',
                    'shape': div['hidden_shape'],
                    'color': div['bull_color'],
                    'text': ''
                })
        
        # Process regular bearish signals
        if 'regular_bear_col' in div and div['regular_bear_col'] in df.columns:
            reg_bear_mask = df[div['regular_bear_col']].fillna(False).astype(bool)
            for _, row in df[reg_bear_mask].iterrows():
                markers.append({
                    'time': row['date'],
                    'position': 'above',
                    'shape': div['regular_shape'],
                    'color': div['bear_color'],
                    'text': ''
                })
        
        # Process hidden bearish signals
        if 'hidden_bear_col' in div and div['hidden_bear_col'] in df.columns:
            hid_bear_mask = df[div['hidden_bear_col']].fillna(False).astype(bool)
            for _, row in df[hid_bear_mask].iterrows():
                markers.append({
                    'time': row['date'],
                    'position': 'above',
                    'shape': div['hidden_shape'],
                    'color': div['bear_color'],
                    'text': ''
                })
    
    # Add all markers in one pass (sorted chronologically)
    if markers:
        subchart.marker_list(sorted(markers, key=lambda x: x['time']))
