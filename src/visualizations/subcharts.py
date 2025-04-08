import pandas as pd
import numpy as np
from lightweight_charts import Chart
from src.visualizations.utils.detect_interval import detect_interval
import time

def calculate_avwap(df, anchor_index):
    """Calculate anchored VWAP (same as before)"""
    df_anchored = df.iloc[anchor_index:].copy()
    df_anchored['cumulative_volume'] = df_anchored['volume'].cumsum()
    df_anchored['cumulative_volume_price'] = (df_anchored['volume'] * 
        (df_anchored['high'] + df_anchored['low'] + df_anchored['close']) / 3).cumsum()
    df_anchored['avwap'] = df_anchored['cumulative_volume_price'] / df_anchored['cumulative_volume']
    return df_anchored['avwap']

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

        # Fair Value Gaps (FVG) - Simplified Visualization -----------------------------------------------

        if all(col in df.columns for col in ['FVG', 'FVG_Top', 'FVG_Bottom', 'FVG_Mitigated_Index']):
            fvg_mask = df['FVG'] != 0
            fvg_dates = df.loc[fvg_mask, 'date']
            fvg_tops = df.loc[fvg_mask, 'FVG_Top']
            fvg_bottoms = df.loc[fvg_mask, 'FVG_Bottom']
            fvg_directions = df.loc[fvg_mask, 'FVG']
            fvg_mitigations = df.loc[fvg_mask, 'FVG_Mitigated_Index']

            # Track unmitigated FVGs to limit them
            unmitigated_fvgs = []
            
            # First pass: Collect all unmitigated FVGs
            for idx in df[fvg_mask].index:
                mitigation_idx = int(df.loc[idx, 'FVG_Mitigated_Index'])
                if mitigation_idx <= 0 or mitigation_idx >= len(df):
                    unmitigated_fvgs.append(idx)
            
            # Only keep the most recent 5 unmitigated FVGs
            if len(unmitigated_fvgs) > 5:
                unmitigated_fvgs = unmitigated_fvgs[-5:]

            # Second pass: Visualize only dashed FVG lines
            for idx in df[fvg_mask].index:
                start_date = df.loc[idx, 'date']
                mitigation_idx = int(df.loc[idx, 'FVG_Mitigated_Index'])
                
                # Skip if this is an unmitigated FVG beyond our limit
                if (mitigation_idx <= 0 or mitigation_idx >= len(df)) and idx not in unmitigated_fvgs:
                    continue
                    
                # Determine end date
                if mitigation_idx <= 0 or mitigation_idx >= len(df):
                    end_date = df.iloc[-1]['date']  # Extend to last candle for unmitigated FVGs
                else:
                    end_date = df.loc[mitigation_idx, 'date']  # Use mitigation candle

                # Color based on FVG direction
                color = 'rgba(39,157,130,255)' if df.loc[idx, 'FVG'] == 1 else 'rgba(200,97,100,255)'

                # Create only the relevant dashed line
                if df.loc[idx, 'FVG'] == 1:  # Bullish FVG - show top line only
                    line = subchart.create_line(
                        price_line=False,
                        price_label=False,
                        color=color,
                        width=1,
                        style='dashed'
                    )
                    line.set(pd.DataFrame({
                        'date': [start_date, end_date],
                        'value': [df.loc[idx, 'FVG_Top'], df.loc[idx, 'FVG_Top']]
                    }))
                else:  # Bearish FVG - show bottom line only
                    line = subchart.create_line(
                        price_line=False,
                        price_label=False,
                        color=color,
                        width=1,
                        style='dashed'
                    )
                    line.set(pd.DataFrame({
                        'date': [start_date, end_date],
                        'value': [df.loc[idx, 'FVG_Bottom'], df.loc[idx, 'FVG_Bottom']]
                    }))
 
        # Peaks, Valleys, Gaps, aVWAPs ----------------------------------------

        # Dynamically find key points based on available columns
        anchor_points = []
       
        # Check for and add peaks if column exists
        if 'Peaks' in df.columns:
            peaks = df[df['Peaks'] == 1].index.tolist()
            anchor_points.extend(peaks)
       
        # Check for and add valleys if column exists
        if 'Valleys' in df.columns:
            valleys = df[df['Valleys'] == 1].index.tolist()
            anchor_points.extend(valleys)
       
        # Check for and add gaps if columns exist
        if 'Gap_Up' in df.columns:
            gaps_up = df[df['Gap_Up'] == 1].index.tolist()
            anchor_points.extend(gaps_up)
        if 'Gap_Down' in df.columns:
            gaps_down = df[df['Gap_Down'] == 1].index.tolist()
            anchor_points.extend(gaps_down)

        # Calculate aVWAPs only if we have anchor points
        avwap_columns = {}
        if anchor_points:
            avwap_columns = {
                f'avwap_{i}': calculate_avwap(df, i)
                for i in anchor_points
            }
            df = pd.concat([df, pd.DataFrame(avwap_columns)], axis=1)
           
            # Calculate average only if we have aVWAP columns
            avwap_cols = [c for c in df.columns if c.startswith('avwap_')]
            if avwap_cols:
                df['aVWAP_avg'] = df[avwap_cols].mean(axis=1)

        # Price line colors
        alpha = 0.5
        line_colors = {
            'peaks': f"rgba(255,165,0,{alpha})",
            'gaps': f"rgba(100,100,100,{alpha}-0.25)",
            'avg': f"rgba(255,165,0,{alpha})",
            'sma': '#87CEEB',  # Sky blue for SMAs
            'supertrend_upper': '#D2042D',  # Red for upper band
            'supertrend_lower': '#0BDA51',  # Green for lower band
            'supertrend_active': '#000000'  # black for reverse-active band
        }
 
        # Plot Supertrend bands if columns exist
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
 
        # Plot all SMA_* columns as blue lines
        sma_cols = [col for col in df.columns if col.startswith('SMA_')]
        for sma_col in sma_cols:
            sma_line = subchart.create_line(
                price_line=False, 
                price_label=False,
                color=line_colors['sma'],
                width=2
            )
            sma_line.set(df[['date', sma_col]].rename(columns={sma_col: 'value'}))
 
        # Plot aVWAP lines if we have anchor points
        if anchor_points:
            for idx in anchor_points:
                # Determine line color based on which marker was found
                if 'Peaks' in df.columns and idx in peaks:
                    color = line_colors['peaks']
                elif 'Valleys' in df.columns and idx in valleys:
                    color = line_colors['peaks']  # same as peaks
                elif ('Gap_Up' in df.columns and idx in gaps_up) or \
                     ('Gap_Down' in df.columns and idx in gaps_down):
                    color = line_colors['gaps']
                else:
                    continue
                   
                avwap_line = subchart.create_line(price_line=False, price_label=False, 
                                                color=color)
                avwap_line.set(df[['date', f'avwap_{idx}']].rename(columns={f'avwap_{idx}': 'value'}))
 
            # Plot average line if it exists
            if 'aVWAP_avg' in df.columns:
                avg_line = subchart.create_line(price_line=False, price_label=False,
                                              color=line_colors['avg'], width=10.0)
                avg_line.set(df[['date', 'aVWAP_avg']].rename(columns={'aVWAP_avg': 'value'}))

        # Format + add chart elements
        subchart.fit()
        subchart.topbar.button('max', 'FULLSCREEN', align='left', separator=True, func=lambda c=subchart: on_max(c, charts))
        subchart.topbar.textbox('ticker', f"{ticker}")
        subchart.topbar.textbox('interval', f"{interval}")
        subchart.grid(False, False)
        subchart.price_line(True, False)
        subchart.price_scale(scale_margin_top=0.05, scale_margin_bottom=0.05)
        subchart.volume_config(up_color=line_colors['peaks'], down_color=line_colors['peaks'], scale_margin_bottom=0.0, scale_margin_top=1.0)
        if show_volume!=True: df = df.drop(columns=['volume'])
        
        subchart.set(df)

    main_chart.show(block=True)
