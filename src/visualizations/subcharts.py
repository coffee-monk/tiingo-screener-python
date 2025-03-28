# import pandas as pd
# from lightweight_charts import Chart
# from src.visualizations.utils.detect_interval import detect_interval
#
# # ASCII button symbols
# FULLSCREEN = '■'
# CLOSE = '×'
#
# def calculate_avwap(df, anchor_index):
#     """
#     Calculate the anchored VWAP (aVWAP) starting from a specific anchor index.
#     """
#     df_anchored = df.iloc[anchor_index:].copy()
#     df_anchored['cumulative_volume'] = df_anchored['volume'].cumsum()
#     df_anchored['cumulative_volume_price'] = (df_anchored['volume'] * (df_anchored['high'] + df_anchored['low'] + df_anchored['close']) / 3).cumsum()
#     df_anchored['avwap'] = df_anchored['cumulative_volume_price'] / df_anchored['cumulative_volume']
#     return df_anchored['avwap']
#
# def on_max(target_chart, charts):
#     """
#     Handle the maximize/restore button click event.
#     """
#     button = target_chart.topbar['max']
#     if button.value == CLOSE:
#         [c.resize(0.5, 0.5) for c in charts]
#         button.set(FULLSCREEN)
#     else:
#         for chart in charts:
#             width, height = (1, 1) if chart == target_chart else (0, 0)
#             chart.resize(width, height)
#         button.set(CLOSE)
#
# def subcharts(df_list, ticker=''):
#     """
#     Visualize 4 different DataFrames in separate subcharts, each with its own aVWAPs.
#     """
#     if len(df_list) != 4:
#         raise ValueError("The input must be a list of exactly 4 DataFrames.")
#
#     # Create main chart and subcharts
#     main_chart = Chart(inner_width=0.5, inner_height=0.5)
#     charts = [
#         main_chart,  # Top-left subchart
#         main_chart.create_subchart(position='right', width=0.5, height=0.5),  # Top-right subchart
#         main_chart.create_subchart(position='left', width=0.5, height=0.5),  # Bottom-left subchart
#         main_chart.create_subchart(position='right', width=0.5, height=0.5)  # Bottom-right subchart
#     ]
#
#     # Process each DataFrame and plot in its respective subchart
#     for i, (df, subchart) in enumerate(zip(df_list, charts)):
#         # Rename columns and format date
#         df.rename(columns={
#             'Open': 'open',
#             'Close': 'close',
#             'Low': 'low',
#             'High': 'high',
#             'Volume': 'volume',
#         }, inplace=True)
#         df = df.reset_index()
#         df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
#
#         # Find peaks, valleys, and gaps
#         peaks = df[df['Peaks'] == 1].index.tolist()
#         valleys = df[df['Valleys'] == 1].index.tolist()
#         gaps = df[(df['Gap_Up'] == 1) | (df['Gap_Down'] == 1)].index.tolist()
#
#         # Collect all aVWAP columns in a dictionary
#         avwap_columns = {}
#         for anchor_index in peaks + valleys + gaps:
#             avwap_columns[f'avwap_{anchor_index}'] = calculate_avwap(df, anchor_index)
#
#         # Add all aVWAP columns to the DataFrame at once
#         df = pd.concat([df, pd.DataFrame(avwap_columns)], axis=1)
#
#         # Calculate the average of all aVWAPs
#         avwap_columns = [col for col in df.columns if col.startswith('avwap_')]
#         df['aVWAP_avg'] = df[avwap_columns].mean(axis=1)
#
#         # Add aVWAP lines to the subchart
#         alpha = 0.5  # Fixed transparency
#         for anchor_index in peaks + valleys:
#             avwap_series = df[['date', f'avwap_{anchor_index}']].rename(columns={f'avwap_{anchor_index}': 'value'})
#             avwap_line = subchart.create_line(price_line=False, price_label=False, color=f"rgba(255,165,0,{alpha})")
#             avwap_line.set(avwap_series)
#
#         for anchor_index in gaps:
#             avwap_series = df[['date', f'avwap_{anchor_index}']].rename(columns={f'avwap_{anchor_index}': 'value'})
#             avwap_line = subchart.create_line(price_line=False, price_label=False, color=f"rgba(100,100,100,{alpha})")
#             avwap_line.set(avwap_series)
#
#         # Add the aVWAP_avg line
#         avwap_avg_series = df[['date', 'aVWAP_avg']].rename(columns={'aVWAP_avg': 'value'})
#         avwap_avg_line = subchart.create_line(price_line=False, price_label=False, color='yellow')
#         avwap_avg_line.set(avwap_avg_series)
#
#         # Add topbar and format subchart
#         subchart.topbar.textbox('ticker', ticker)
#         subchart.topbar.button('max', FULLSCREEN, False, align='left', func=lambda c=subchart: on_max(c, charts))
#
#         # Set the candlestick data
#         subchart.set(df)
#
#     main_chart.show(block=True)











import pandas as pd
from lightweight_charts import Chart
from collections import Counter
from src.visualizations.utils.detect_interval import detect_interval
import time

# ASCII button symbols
FULLSCREEN = 'FULLSCREEN'
CLOSE = 'MINIMIZE'

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
    if button.value == CLOSE:
        [c.resize(0.5, 0.5) for c in charts]
        button.set(FULLSCREEN)
    else:
        for chart in charts:
            width, height = (1.0, 1.0) if chart == target_chart else (0.0, 0.0)
            chart.resize(width, height)
            chart.fit()
        button.set(CLOSE)

def subcharts(df_list, ticker=''):
    """
    Visualize 4 different DataFrames with automatic interval detection.
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
  
        # Get metadata
        start_date = df['date'].iloc[0].strftime('%Y-%m-%d') if not df.empty else 'N/A'
        interval = detect_interval(df)
  
        # Format for display
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Find key points
        peaks = df[df['Peaks'] == 1].index.tolist()
        valleys = df[df['Valleys'] == 1].index.tolist()
        gaps = df[(df['Gap_Up'] == 1) | (df['Gap_Down'] == 1)].index.tolist()

        # Calculate aVWAPs
        avwap_columns = {
            f'avwap_{i}': calculate_avwap(df, i)
            for i in peaks + valleys + gaps
        }
        df = pd.concat([df, pd.DataFrame(avwap_columns)], axis=1)
        df['aVWAP_avg'] = df[[c for c in df.columns if c.startswith('avwap_')]].mean(axis=1)

        # Format + add chart elements
        subchart.fit()
        subchart.topbar.button('max', FULLSCREEN, align='left', separator=True, func=lambda c=subchart: on_max(c, charts))
        # subchart.topbar.textbox('info', f"{ticker} | {interval}")
        subchart.topbar.textbox('ticker', f"{ticker}")
        subchart.topbar.textbox('interval', f"{interval}")
        # subchart.topbar.textbox('start_date', f"{start_date}")
        # subchart.topbar.textbox('info', f"{ticker}")
        # subchart.watermark(f"{ticker} | {interval}")
        # subchart.watermark(f"{start_date}")
        # subchart.topbar.textbox('ticker', ticker)

        # Price line colors
        alpha = 0.5
        line_colors = {
            'peaks': f"rgba(255,165,0,{alpha})",
            'gaps': f"rgba(100,100,100,{alpha})",
            'avg': 'yellow'
        }
  
        for idx in peaks + valleys:
            avwap_line = subchart.create_line(price_line=False, price_label=False, 
                                            color=line_colors['peaks'])
            avwap_line.set(df[['date', f'avwap_{idx}']].rename(columns={f'avwap_{idx}': 'value'}))
  
        for idx in gaps:
            gap_line = subchart.create_line(price_line=False, price_label=False,
                                          color=line_colors['gaps'])
            gap_line.set(df[['date', f'avwap_{idx}']].rename(columns={f'avwap_{idx}': 'value'}))
  
        avg_line = subchart.create_line(price_line=False, price_label=False,
                                      color=line_colors['avg'])
        avg_line.set(df[['date', 'aVWAP_avg']].rename(columns={'aVWAP_avg': 'value'}))

        subchart.set(df)

    main_chart.show(block=True)
