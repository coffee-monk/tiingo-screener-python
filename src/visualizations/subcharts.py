import pandas as pd
import numpy as np
from lightweight_charts import Chart
from src.visualizations.utils.detect_interval import detect_interval
import time

def on_max(target_chart, charts):
    """
    Handle the maximize/restore button click event
    """
    button = target_chart.topbar['max']
    if button.value == 'MINIMIZE':
        [c.resize(0.5, 0.5) for c in charts]
        button.set('FULLSCREEN')
    else:
        for chart in charts:
            width, height = (1.0, 1.0) if chart == target_chart else (0.0, 0.0)
            chart.resize(width, height)
            chart.fit()
        button.set('MINIMIZE')

def subcharts(df_list, ticker='', show_volume=False):
    """
    Visualize 4 different DataFrames with automatic interval detection.
    Now includes both Upper and Lower Supertrend bands, SMA, peaks/valleys/gap columns.
    """
    if len(df_list) != 4:
        raise ValueError("The input must be a list of exactly 4 DataFrames.")

    # Create main chart and subcharts
    main_chart = Chart(inner_width=0.5, inner_height=0.5, maximize=True)
    charts = [
        main_chart,
        main_chart.create_subchart(width=0.5, height=0.5, position='left'),
        main_chart.create_subchart(width=0.5, height=0.5, position='left'),
        main_chart.create_subchart(width=0.5, height=0.5, position='right')
    ]

    # Price line colors
    alpha = 0.25
    line_colors = {
        'aVWAP': f"rgba(255,165,0,{alpha})",
        'peaks': f"rgba(255,165,0,{alpha})",
        'gaps': f"rgba(100,100,100,{alpha}-0.25)",
        'avg': f"rgba(255,165,0,{alpha})",
        'sma': '#87CEEB',  # Sky blue for SMAs
        'supertrend_upper': '#D2042D',  # Red for upper band
        'supertrend_lower': '#0BDA51',  # Green for lower band
        'supertrend_active': '#000000'  # black for reverse-active band
    }

    for i, (df, subchart) in enumerate(zip(df_list, charts)):
        # Rename columns and ensure datetime format
        df = df.rename(columns={
            'Open': 'open',
            'Close': 'close',
            'Low': 'low',
            'High': 'high',
            'Volume': 'volume'
        }).copy()
        df = df.reset_index()
        df['date'] = pd.to_datetime(df['date'])
 
        # Get dataframe metadata
        start_date = df['date'].iloc[0].strftime('%Y-%m-%d') if not df.empty else 'N/A'
        interval = detect_interval(df)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S') # Format for display

        # Fair Value Gaps (FVG) -----------------------------------------------

        if all(col in df.columns for col in ['FVG', 'FVG_Top', 'FVG_Bottom', 'FVG_Mitigated_Index']):
            # Get all FVG indices sorted by date (newest first)
            fvg_indices = df[df['FVG'] != 0].index[::-1]
            
            # Separate into mitigated and unmitigated
            mitigated = []
            unmitigated = []
            
            for idx in fvg_indices:
                mit_idx = int(df.loc[idx, 'FVG_Mitigated_Index'])
                if 0 < mit_idx < len(df):
                    mitigated.append(idx)
                else:
                    unmitigated.append(idx)
            
            # Take limited number of most recent mitigated and unmitigated
            show_indices = mitigated[:20] + unmitigated[:10]
            
            for idx in show_indices:
                mit_idx = int(df.loc[idx, 'FVG_Mitigated_Index'])
                level = 'FVG_Top' if df.loc[idx, 'FVG'] == 1 else 'FVG_Bottom'
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

        # Order Blocks (OB) ---------------------------------------------------

        if all(col in df.columns for col in ['OB', 'OB_Top', 'OB_Bottom']):
            for idx in df[df['OB'] != 0].index:
                start_date = df.loc[idx, 'date']
                
                # Calculate midpoint between top and bottom
                midpoint = (df.loc[idx, 'OB_Top'] + df.loc[idx, 'OB_Bottom']) / 2
                
                # Determine end date
                end_date = (df.loc[mitigation_idx, 'date'] if 'OB_Mitigated_Index' in df.columns 
                           and 0 < (mitigation_idx := int(df.loc[idx, 'OB_Mitigated_Index'])) < len(df)
                           else df.iloc[-1]['date'])
                
                # Draw single wider midpoint line
                subchart.create_line(
                    price_line=False,
                    price_label=False,
                    color='rgba(39,157,130,0.4)' if df.loc[idx, 'OB'] == 1 else 'rgba(200,97,100,0.4)',
                    width=10,  # Wider line
                    style='solid'
                ).set(pd.DataFrame({
                    'date': [start_date, end_date],
                    'value': [midpoint, midpoint]
                }))

        # BoS/CHoCH Visualization ---------------------------------------------

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

        # Liquidity Level Visualization ---------------------------------------

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
                    color='rgba(255,255,0,0.25)',
                    width=1,
                    style='solid'
                ).set(pd.DataFrame({
                    'date': [df.iloc[0]['date'], df.iloc[-1]['date']],  # Full chart width
                    'value': [level, level]  # Constant price level
                }))

        # Peaks, Valleys, Gaps, aVWAPs ----------------------------------------

        # Plot aVWAP Channel --------------------------------------------------

        avwap_cols = [col for col in df.columns if col.startswith('aVWAP_') and not col.endswith('_avg')]
        
        if avwap_cols:
            # Plot all aVWAP lines
            for col in avwap_cols:
                avwap_line = subchart.create_line(
                    price_line=False,
                    price_label=False,
                    color=line_colors['aVWAP'],
                    width=1
                )
                avwap_line.set(df[['date', col]].rename(columns={col: 'value'}))
            
            # Plot average line if it exists
            if 'aVWAP_avg' in df.columns:
                avg_line = subchart.create_line(
                    price_line=False,
                    price_label=False,
                    color=line_colors['aVWAP'],
                    width=2  # Slightly thicker for average line
                )
                avg_line.set(df[['date', 'aVWAP_avg']].rename(columns={'aVWAP_avg': 'value'}))

        # Plot Supertrend bands if columns exist ------------------------------

        if all(col in df.columns for col in ['Supertrend_Upper', 'Supertrend_Lower', 'Supertrend_Direction']):
            # Upper band (resistance in downtrend)
            upper_line = subchart.create_line(
                price_line=False,
                price_label=False,
                color=line_colors['supertrend_upper'],
                width=1.0,
            )
            upper_line.set(df[['date', 'Supertrend_Upper']].rename(columns={'Supertrend_Upper': 'value'}))
            
            # Lower band (support in uptrend)
            lower_line = subchart.create_line(
                price_line=False,
                price_label=False,
                color=line_colors['supertrend_lower'],
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
                color=line_colors['supertrend_active'],
                width=2.0  # Thicker to cover upper/lower bands for visualization
            )
            active_line.set(df[['date']].assign(value=active_supertrend))
 
        # Plot Simple Moving Average (SMA) ------------------------------------

        sma_cols = [col for col in df.columns if col.startswith('SMA_')]
        for sma_col in sma_cols:
            sma_line = subchart.create_line(
                price_line=False, 
                price_label=False,
                color=line_colors['sma'],
                width=2
            )
            sma_line.set(df[['date', sma_col]].rename(columns={sma_col: 'value'}))
 
        # Format + Set Chart ==================================================

        subchart.fit()
        subchart.topbar.button('max', 'FULLSCREEN', align='left', separator=True, func=lambda c=subchart: on_max(c, charts))
        subchart.topbar.textbox('ticker', f"{ticker}")
        subchart.topbar.textbox('interval', f"{interval}")
        subchart.grid(False, False)
        subchart.price_line(True, False)
        subchart.price_scale(scale_margin_top=0.05, scale_margin_bottom=0.05)
        subchart.volume_config(up_color=line_colors['peaks'], down_color=line_colors['peaks'], scale_margin_bottom=0.0, scale_margin_top=1.0)
        if not show_volume: df = df.drop(columns=['volume']) 
        
        # print(df.columns)
        # print(df.head(10))
        # print(df.tail(10))
        subchart.set(df)

    main_chart.show(block=True)
