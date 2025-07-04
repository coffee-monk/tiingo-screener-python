import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from datetime import datetime
from lightweight_charts import Chart
from src.visualization.src.color_palette import get_color_palette
from src.visualization.src.indicators import add_visualizations

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "data" / "indicators"


def prepare_dataframe(df, show_volume, padding_ratio=0.25):
    """
    Prepare dataframe with dynamic padding based on chart length.
    Adds padding candles equal to 25% (or custom ratio) of current candle count.
   
    Args:
        df: Input DataFrame
        show_volume: Whether to include volume column
        padding_ratio: Fraction of current candles to add as padding (default 0.25 = 25%)
    """
    df = df.copy()
   
    # Rename columns
    df = df.rename(columns={
        'Open': 'open',
        'Close': 'close', 
        'Low': 'low',
        'High': 'high',
        'Volume': 'volume'
    })
   
    # Store original timeframe
    timeframe = df.attrs['timeframe']
   
    # Reset index and convert date
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])
   
    # Calculate dynamic padding length (25% of current candles, rounded up)
    if padding_ratio > 0 and len(df) > 0:
        padding_candles = max(5, int(len(df) * padding_ratio))  # Minimum 5 candles
        last_candle = df.iloc[-1].copy()
        last_date = last_candle['date']
       
        # Convert timeframe to pandas frequency
        tf = str(timeframe).lower()
        tf_mapping = {
            '1min': '1min', '5min': '5min', '15min': '15min', '30min': '30min',
            '1h': '1H', '1hour': '1H', '4h': '4H', '4hour': '4H',
            'd': '1D', 'day': '1D', 'daily': '1D',
            'w': '1W', 'week': '1W', 'weekly': '1W'
        }
        freq = tf_mapping.get(tf, '1D')
       
        # Generate future dates
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(freq),
            periods=padding_candles,
            freq=freq
        )
       
        # Create invisible padding candles
        future_df = pd.DataFrame({
            'date': future_dates,
            'open': np.nan,
            'high': np.nan,
            'low': np.nan,
            'close': np.nan,
            'volume': 0
        })
       
        # Carry forward indicators
        indicator_cols = [c for c in df.columns if c.startswith(('aVWAP','OB'))]
        for col in indicator_cols:
            future_df[col] = last_candle.get(col, np.nan)
       
        df = pd.concat([df, future_df], ignore_index=True)
   
    # Format dates for display
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
   
    # Handle volume column
    if not show_volume and 'volume' in df.columns:
        df = df.drop(columns=['volume'])
   
    return df, timeframe


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
        # Side-by-side layout for 2 charts
        main_chart = Chart(inner_width=0.5, inner_height=1.0, maximize=True)
        charts = [
            main_chart,
            main_chart.create_subchart(width=0.5, height=1.0, position='right')
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


KEY_MAPPINGS = {
    '-': 0,
    '=': 1,
    '[': 2,
    ']': 3,
}


def add_ui_elements(chart, charts, ticker, timeframe, show_volume=False):
    """
    Add UI elements like buttons and hotkeys.
    """
    try:
        if chart.topbar is not None:
           chart.topbar['ticker'].set(ticker)
           chart.topbar['timeframe'].set(timeframe)
    except KeyError:
        i = int(chart.name)
        chart.topbar.textbox('ticker', ticker)
        chart.topbar.textbox('timeframe', timeframe)
        if len(charts) > 1:
            chart.topbar.button('max', 'FULLSCREEN', align='left', separator=True, 
                               func=lambda c=chart: _maximize_minimize_button(c, charts))
       
        # Hotkeys
        chart.hotkey(None, ' ', lambda key=' ': _maximize_minimize_hotkey(charts, key))
        chart.hotkey('ctrl', 'c', lambda: sys.exit(1))
        chart.events.search += _on_search
        chart.hotkey(None, str(1+i), lambda key=str(1+i): _maximize_minimize_hotkey(charts, key))
        # charts hotkeys
        chart.hotkey(None, str(i+6), lambda key=i: _load_timeframe_csv(charts, key, show_volume))
        # tickers hotkeys
        if i == 0: chart.hotkey(None, '-', lambda key='-': _load_ticker_csv(charts, key, show_volume))
        if i == 1: chart.hotkey(None, '=', lambda key='=': _load_ticker_csv(charts, key, show_volume))
        if i == 2: chart.hotkey(None, '[', lambda key='[': _load_ticker_csv(charts, key, show_volume))
        if i == 3: chart.hotkey(None, ']', lambda key=']': _load_ticker_csv(charts, key, show_volume))
        # screenshot hotkeys
        if i == 0: chart.hotkey(None, '_', lambda key='_': _take_screenshot(charts, key))
        if i == 1: chart.hotkey(None, '+', lambda key='+': _take_screenshot(charts, key))
        if i == 2: chart.hotkey(None, '{', lambda key='{': _take_screenshot(charts, key))
        if i == 3: chart.hotkey(None, '}', lambda key='}': _take_screenshot(charts, key))


def _maximize_minimize_hotkey(charts, key):
        """Maximize the specified chart (1-4) or reset all (space)"""
        if key == ' ':
            # Reset all charts to normal size
            default_chart_dimensions = _get_default_chart_dimensions()
            for chart, (width, height) in zip(charts, default_chart_dimensions[len(charts)]):
                chart.resize(width, height)
                chart.fit()
            for chart in charts:
                try: chart.topbar['max'].set('FULLSCREEN') 
                except KeyError: pass
        elif key in ('1', '2', '3', '4'):
            idx = int(key) - 1
            # Maximize selected chart, minimize others
            for i, chart in enumerate(charts):
                width, height = (1.0, 1.0) if i == idx else (0.0, 0.0)
                chart.resize(width, height)
                chart.fit()
                # Update button text
                try: chart.topbar['max'].set('MINIMIZE' if i == idx else 'FULLSCREEN')
                except KeyError: pass


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


def _get_default_chart_dimensions():
    return {
        1: [(1.0, 1.0)],
        2: [(0.5, 1.0), (0.5, 1.0)],  # Side-by-side for 2 charts
        3: [(1.0, 0.5), (0.5, 0.5), (0.5, 0.5)],
        4: [(0.5, 0.5)] * 4
    }


def _on_search(chart, input_ticker):
    print(f"Searching for ticker: {input_ticker}")
   
    try:
        # Get current timeframe from chart
        current_timeframe = chart.topbar['timeframe'].value
       
        # Search for files matching both ticker and current timeframe
        matching_files = sorted(DATA_ROOT.glob(f"{input_ticker}_{current_timeframe}_*.csv"), reverse=True)
       
        if not matching_files:
            print(f"No {current_timeframe} data found for {input_ticker}")
            return  # Keep current chart as is
       
        # Load the most recent matching file
        selected_file = matching_files[0]
        print(f"Loading data from: {selected_file}")
       
        try:
            df = pd.read_csv(selected_file)
            df = df.rename(columns={
                'Open': 'open',
                'Close': 'close', 
                'Low': 'low',
                'High': 'high'
            }).copy()
           
            # Set timeframe attribute (should match current_timeframe)
            df.attrs['timeframe'] = current_timeframe
           
            # Update chart
            lines = chart.lines()
            for line in lines: line.hide_data()
            chart.clear_markers()
            configure_base_chart(df, chart)
            add_ui_elements(chart, [chart], input_ticker, current_timeframe, False)
            add_visualizations(chart, df, False)
            chart.set(None)
            chart.set(df)
            chart.fit()
           
        except Exception as e:
            print(f"Error loading data: {e}")
           
    except KeyError:
        print("Could not determine current timeframe from chart")
    except Exception as e:
        print(f"Error during search: {e}")


def _load_timeframe_csv(charts, key, show_volume=False):
    # Get current values from topbar
    print(key)
    chart = charts[int(key)-6]
    ticker = chart.topbar['ticker'].value
    current_timeframe = chart.topbar['timeframe'].value

    # Define all possible timeframes in preferred order
    timeframe_order = ['weekly', 'daily', '4hour', '1hour', '30min', '15min', '5min', '1min']
   
    # Find available timeframes for this ticker
    available_timeframes = []
    for tf in timeframe_order:
        if list(DATA_ROOT.glob(f"{ticker}_{tf}_*.csv")):
            available_timeframes.append(tf)
   
    if not available_timeframes:
        print(f"No timeframe data found for {ticker}")
        return

    # Find current position in AVAILABLE timeframes
    try:
        current_index = available_timeframes.index(current_timeframe)
    except ValueError:
        current_index = -1  # Current timeframe not available
       
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
    for line in lines: line.set(pd.DataFrame())
    chart.clear_markers()
    configure_base_chart(df, chart)
    add_ui_elements(chart, [chart], ticker, next_timeframe, show_volume)
    add_visualizations(chart, df, False)
    chart.set(df)
    chart.fit()


def _load_ticker_csv(charts, key, show_volume=False):
    """
    Simplified version that always loads from indicators directory
    """
    from src.visualization.subcharts import CURRENT_SCAN_FILE
    from pathlib import Path
    import pandas as pd

    KEY_MAPPINGS = {'-': 0, '=': 1, '[': 2, ']': 3}

    try:
        # Get the target chart
        chart_index = KEY_MAPPINGS[key]
        chart = charts[chart_index]
        
        # Get current values from chart
        current_ticker = chart.topbar['ticker'].value
        timeframe = chart.topbar['timeframe'].value
        
        # Default behavior: cycle all tickers with indicator data
        ticker_files = sorted(Path("data/indicators").glob(f"*_{timeframe}_*.csv"))
        available_tickers = sorted(list({f.name.split('_')[0] for f in ticker_files}))
        
        if not available_tickers:
            print(f"No tickers available for {timeframe} timeframe")
            return

        # Find next ticker in sequence
        try:
            current_index = available_tickers.index(current_ticker)
            next_index = (current_index + 1) % len(available_tickers)
        except ValueError:
            next_index = 0  # Current ticker not in list
        
        next_ticker = available_tickers[next_index]
        
        # Load the indicator data
        indicator_file = next(Path("data/indicators").glob(f"{next_ticker}_{timeframe}_*.csv"), None)
        if not indicator_file:
            print(f"No indicator data found for {next_ticker} {timeframe}")
            return
            
        # Update the chart
        df = pd.read_csv(indicator_file).rename(columns={
            'Open': 'open',
            'Close': 'close',
            'Low': 'low', 
            'High': 'high'
        })
        df.attrs = {'timeframe': timeframe, 'ticker': next_ticker}
        
        # Clear existing elements
        for line in chart.lines():
            line.set(pd.DataFrame())
        chart.clear_markers()

        # Reconfigure chart
        prepared_df, _ = prepare_dataframe(df, show_volume)
        configure_base_chart(prepared_df, chart)
        add_ui_elements(chart, charts, next_ticker, timeframe, show_volume)
        add_visualizations(chart, prepared_df, False)
        chart.set(prepared_df)
        chart.fit()
        
        print(f"Loaded {next_ticker} ({timeframe}) from {indicator_file.name}")

    except Exception as e:
        print(f"Error during ticker cycling: {str(e)}")


def get_most_recent_scanner_file():
    """Find newest scanner file in scanner/ folder"""
    scanner_path = DATA_ROOT.parent / "scanner"
    if not scanner_path.exists():
        return None
       
    scan_files = sorted(
        scanner_path.glob("scan_results_*.csv"),
        key=lambda x: x.stem.split('_')[-1],  # Sort by date in filename
        reverse=True
    )
    return scan_files[0] if scan_files else None


def find_indicator_file(ticker, timeframe):
    """Find newest indicator file for ticker+timeframe"""
    files = sorted(DATA_ROOT.glob(f"{ticker}_{timeframe}_*.csv"), reverse=True)
    return files[0] if files else None


SCREENSHOT_KEY_MAPPINGS = {
    '_': 0,  # Shift + - (underscore)
    '+': 1,  # Shift + = (plus)
    '{': 2,  # Shift + [ (left curly brace)
    '}': 3   # Shift + ] (right curly brace)
}


def _take_screenshot(charts, key, screenshot_dir=None):
    """
    Take a screenshot of the specified chart and save it to the screenshots folder.
    
    Args:
        charts: List of chart objects
        key: Hotkey pressed (maps to chart index)
        screenshot_dir: Optional custom directory to save screenshots
    """
    try:
        chart_index = SCREENSHOT_KEY_MAPPINGS[key]
        chart = charts[chart_index]
    except (KeyError, IndexError) as e:
        print(f"Invalid key or chart index: {e}")
        return
    
    # Create screenshots directory if it doesn't exist
    if screenshot_dir is None:
        screenshot_dir = Path.cwd() / 'data' / 'screenshots'
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    # Get current ticker and timeframe for filename
    ticker = chart.topbar['ticker'].value
    timeframe = chart.topbar['timeframe'].value
    timestamp = datetime.now().strftime('%d%m%y_%H%M%S')
    
    # Create filename
    filename = f"{ticker}_{timeframe}_{timestamp}.png"
    filepath = screenshot_dir / filename
    
    # Take and save screenshot
    try:
        img = chart.screenshot()
        with open(filepath, 'wb') as f:
            f.write(img)
        print(f"Screenshot saved to: {filepath}")
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
