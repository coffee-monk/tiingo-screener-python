import os
import pandas as pd
from pathlib import Path
from datetime import datetime
from src.visualization.src.subcharts.indicators import add_visualizations
from src.visualization.src.subcharts.charts import (
    get_charts,
    prepare_dataframe, 
    configure_base_chart, 
    add_ui_elements,
)

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "data" / "indicators"

def chart_browser(df='', ticker='', show_volume=False):

    df = pd.read_csv(str(DATA_ROOT) + '/AAPL_1hour_160525.csv')
    df = df.rename(columns={
        'Open': 'open',
        'Close': 'close',
        'Low': 'low',
        'High': 'high',
    }).copy()
    df.attrs['timeframe'] = '1hour'

    main_chart, chart = get_charts([df])

    df, interval = prepare_dataframe(df, show_volume)
    configure_base_chart(df, chart[0], False)
    add_ui_elements(chart[0], chart, ticker, interval)
    add_visualizations(main_chart, df, False)
    main_chart.set(df)

    main_chart.show(block=True)


def load_timeframe(chart, direction):
    # Get current values from topbar
    ticker = chart.topbar['ticker'].value
    current_timeframe = chart.topbar['timeframe'].value
    
    # Define all possible timeframes in preferred order
    timeframe_order = ['1min', '5min', '15min', '30min', '1hour', '4hour', 'daily', 'weekly']
    
    # Find available timeframes for this ticker
    available_timeframes = []
    for tf in timeframe_order:
        if list(DATA_ROOT.glob(f"{ticker}_{tf}_*.csv")):
            available_timeframes.append(tf)
    
    if not available_timeframes:
        print(f"No timeframe data found for {ticker}")
        return

    chart.set(None)
        
    # Find current position in AVAILABLE timeframes
    try:
        current_index = available_timeframes.index(current_timeframe)
    except ValueError:
        current_index = -1  # Current timeframe not available
        
    # # Calculate next timeframe (with wrap-around)
    # print('\n')
    # print(current_index)
    # print(direction)
    # print('\n')

    next_index = (current_index + 1) % len(available_timeframes)
    next_timeframe = available_timeframes[next_index]
    
    # Load the most recent file for this timeframe
    matching_files = sorted(DATA_ROOT.glob(f"{ticker}_{next_timeframe}_*.csv"), reverse=True)
    selected_file = matching_files[0]
    print(f"Loading {ticker} {next_timeframe} data from: {selected_file}")
    
    # Update chart
    df = pd.read_csv(selected_file).rename(columns={
        'Open': 'open', 'Close': 'close', 'Low': 'low', 'High': 'high'
    }).copy()
    df.attrs['timeframe'] = next_timeframe
    
    lines = chart.lines()
    # for line in lines: line.hide_data()
    for line in lines: line.set(pd.DataFrame())
    chart.clear_markers()
    configure_base_chart(df, chart, False)
    add_ui_elements(chart, [chart], ticker, next_timeframe)
    add_visualizations(chart, df, False)
    chart.set(None)
    chart.set(df)
    chart.fit()
