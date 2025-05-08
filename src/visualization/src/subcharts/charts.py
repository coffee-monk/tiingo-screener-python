import pandas as pd
from lightweight_charts import Chart
from src.visualization.src.color_palette import get_color_palette


def prepare_dataframe(df, show_volume):
    # Rename columns and ensure datetime format
    df = df.rename(columns={
        'Open': 'open',
        'Close': 'close',
        'Low': 'low',
        'High': 'high',
        'Volume': 'volume'
    }).copy()
    # Get dataframe metadata
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])
    start_date = df['date'].iloc[0].strftime('%Y-%m-%d') if not df.empty else 'N/A'
    interval = df.attrs['timeframe']
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S') # format dates for display
    if not show_volume: df = df.drop(columns=['volume']) # include/remove volume column for vis
    return df, interval


def configure_base_chart(df, chart):
    df = df.copy()
    colors = get_color_palette()
    scale_margin_bottom = 0.15 if 'volume' in df.columns else 0.05
    if 'volume' in df.columns: scale_margin_bottom = 0.2 if 'banker_RSI' in df.columns else 0.15
    else: scale_margin_bottom = 0.1 if 'banker_RSI' in df.columns else 0.05
    # Apply base configuration to all charts.
    chart.fit()
    chart.candle_style(
        up_color=colors['teal'], 
        down_color=colors['red'],
        border_up_color=colors['teal'], 
        border_down_color=colors['red'],
        wick_up_color=colors['teal'], 
        wick_down_color=colors['red']
    )
    chart.grid(False, False)
    chart.price_line(True, False)
    chart.price_scale(scale_margin_top=0.05, 
                      scale_margin_bottom=scale_margin_bottom)
    chart.volume_config(scale_margin_bottom=0.0, 
                        scale_margin_top=0.9,
                        up_color=colors['orange_volume'],
                        down_color=colors['orange_volume'])


def get_charts(df_list):
    # Validate input
    num_charts = len(df_list)
    if num_charts < 1 or num_charts > 4:
        raise ValueError("Input must contain 1-4 DataFrames")
    # Create charts and layout based on number of DataFrames
    if num_charts == 1:
        main_chart = Chart(inner_width=1.0, inner_height=1.0, maximize=True)
        charts = [main_chart]
    elif num_charts == 2:
        main_chart = Chart(inner_width=1.0, inner_height=0.5, maximize=True)
        charts = [
            main_chart,
            main_chart.create_subchart(width=1.0, height=0.5, position='right')
        ]
    elif num_charts == 3:
        main_chart = Chart(inner_width=1.0, inner_height=0.5, maximize=True)
        charts = [
            main_chart,
            main_chart.create_subchart(width=0.5, height=0.5, position='left'),
            main_chart.create_subchart(width=0.5, height=0.5, position='right')
        ]
    elif num_charts == 4:
        main_chart = Chart(inner_width=0.5, inner_height=0.5, maximize=True)
        charts = [
            main_chart,
            main_chart.create_subchart(width=0.5, height=0.5, position='left'),
            main_chart.create_subchart(width=0.5, height=0.5, position='left'),
            main_chart.create_subchart(width=0.5, height=0.5, position='right')
        ]
    return main_chart, charts


def add_ui_elements(chart, charts, ticker, interval):
    """
    Add UI elements like buttons and hotkeys.
    """
    # Topbar elements
    chart.topbar.textbox('ticker', ticker)
    chart.topbar.textbox('interval', interval)
    chart.topbar.button('max', 'FULLSCREEN', align='left', separator=True, 
                       func=lambda c=chart: _maximize_minimize_button(c, charts))
    
    # Hotkeys
    chart.hotkey(None, ' ', lambda key=' ': _maximize_minimize_hotkey(charts, key))
    chart.hotkey('ctrl', 'c', lambda: sys.exit(0))
    for i in range(1, len(charts) + 1):
        chart.hotkey(None, str(i), lambda key=str(i): _maximize_minimize_hotkey(charts, key))


def _maximize_minimize_button(target_chart, charts):
    button = target_chart.topbar['max']
    if button.value == 'MINIMIZE':
        # Reset all charts to normal size
        default_chart_dimensions = _get_default_chart_dimensions()
        for chart, (width, height) in zip(charts, default_chart_dimensions[len(charts)]):
            chart.resize(width, height)
            chart.fit()
        button.set('FULLSCREEN')
    else:
        # Maximize selected chart, minimize others
        for chart in charts:
            width, height = (1.0, 1.0) if chart == target_chart else (0.0, 0.0)
            chart.resize(width, height)
            chart.fit()
        button.set('MINIMIZE')


def _maximize_minimize_hotkey(charts, key):
        """Maximize the specified chart (1-4) or reset all (space)"""
        if key == ' ':
            # Reset all charts to normal size
            default_chart_dimensions = _get_default_chart_dimensions()
            for chart, (width, height) in zip(charts, default_chart_dimensions[len(charts)]):
                chart.resize(width, height)
                chart.fit()
            for chart in charts:
                chart.topbar['max'].set('FULLSCREEN')
        elif key in ('1', '2', '3', '4'):
            idx = int(key) - 1
            # Maximize selected chart, minimize others
            for i, chart in enumerate(charts):
                width, height = (1.0, 1.0) if i == idx else (0.0, 0.0)
                chart.resize(width, height)
                chart.fit()
                # Update button text
                chart.topbar['max'].set('MINIMIZE' if i == idx else 'FULLSCREEN')


def _get_default_chart_dimensions():
    return {
        1: [(1.0, 1.0)],
        2: [(0.5, 1.0), (0.5, 1.0)],
        3: [(1.0, 0.5), (0.5, 0.5), (0.5, 0.5)],
        4: [(0.5, 0.5)] * 4
    }
