import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from datetime import datetime
from lightweight_charts import Chart
from src.visualization.src.color_palette import get_color_palette
from src.visualization.src.indicator_visualizations import add_visualizations
from config.settings import INDICATORS_DIR

def prepare_dataframe(df, show_volume, padding_ratio=0.25):
    df = df.copy()
    df = df.rename(columns={
        'Open': 'open',
        'Close': 'close', 
        'Low': 'low',
        'High': 'high',
        'Volume': 'volume'
    })
    timeframe = df.attrs['timeframe']
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])
    
    if padding_ratio > 0 and len(df) > 0:
        padding_candles = max(5, int(len(df) * padding_ratio))
        last_candle = df.iloc[-1].copy()
        last_date = last_candle['date']
        tf = str(timeframe).lower()
        tf_mapping = {
            '1min': '1min', '5min': '5min', '15min': '15min', '30min': '30min',
            '1h': '1H', '1hour': '1H', '4h': '4H', '4hour': '4H',
            'd': '1D', 'day': '1D', 'daily': '1D',
            'w': '1W', 'week': '1W', 'weekly': '1W'
        }
        freq = tf_mapping.get(tf, '1D')
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(freq),
            periods=padding_candles,
            freq=freq
        )
        future_df = pd.DataFrame({
            'date': future_dates,
            'open': np.nan,
            'high': np.nan,
            'low': np.nan,
            'close': np.nan,
            'volume': 0
        })
        indicator_cols = [c for c in df.columns if c.startswith(('aVWAP','OB'))]
        for col in indicator_cols:
            future_df[col] = last_candle.get(col, np.nan)
        df = pd.concat([df, future_df], ignore_index=True)
    
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    if not show_volume and 'volume' in df.columns:
        df = df.drop(columns=['volume'])
    return df, timeframe

def configure_base_chart(df, chart, show_volume=False, show_banker_RSI=False):
    colors = get_color_palette()
    scale_margin_bottom = 0.2 if show_banker_RSI and show_volume else 0.15 if show_volume else 0.1 if show_banker_RSI else 0.05
    # scale_margin_bottom = 0.2 if ('volume' in df.columns and 'banker_RSI' in df.columns) else 0.15 if 'volume' in df.columns else 0.1 if 'banker_RSI' in df.columns else 0.05
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
    chart.price_scale(scale_margin_top=0.05, scale_margin_bottom=scale_margin_bottom)
    chart.volume_config(
                        scale_margin_top=0.9,
                        scale_margin_bottom=0.0, 
                        up_color=colors['orange_volume'], 
                        down_color=colors['orange_volume']
                       )

def get_charts(df_list):
    num_charts = len(df_list)
    if num_charts < 1 or num_charts > 4:
        raise ValueError("Input must contain 1-4 DataFrames")
    
    if num_charts == 1:
        main_chart = Chart(inner_width=1.0, inner_height=1.0, maximize=True)
        charts = [
                  main_chart
                 ]
    elif num_charts == 2:
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

KEY_MAPPINGS = {'-':0,'=':1,'[':2,']':3}

def add_ui_elements(chart, charts, ticker, timeframe, show_volume=False, show_banker_RSI=False):
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
        
        chart.events.search += _on_search
        chart.hotkey(None, ' ', lambda key=' ': _maximize_minimize_hotkey(charts, key))
        chart.hotkey('ctrl', 'c', lambda: sys.exit(1))
        chart.hotkey(None, str(1+i), lambda key=str(1+i): _maximize_minimize_hotkey(charts, key))
        chart.hotkey(None, str(i+6), lambda key=i: _load_timeframe_csv(charts, key, show_volume, show_banker_RSI))
        if i == 0: chart.hotkey(None, '-', lambda key='-': _load_ticker_csv(charts, key, show_volume, show_banker_RSI))
        if i == 1: chart.hotkey(None, '=', lambda key='=': _load_ticker_csv(charts, key, show_volume, show_banker_RSI))
        if i == 2: chart.hotkey(None, '[', lambda key='[': _load_ticker_csv(charts, key, show_volume, show_banker_RSI))
        if i == 3: chart.hotkey(None, ']', lambda key=']': _load_ticker_csv(charts, key, show_volume, show_banker_RSI))
        if i == 0: chart.hotkey(None, '_', lambda key='_': _take_screenshot(charts, key))
        if i == 1: chart.hotkey(None, '+', lambda key='+': _take_screenshot(charts, key))
        if i == 2: chart.hotkey(None, '{', lambda key='{': _take_screenshot(charts, key))
        if i == 3: chart.hotkey(None, '}', lambda key='}': _take_screenshot(charts, key))

def _load_ticker_csv(charts, key, show_volume=False, show_banker_RSI=False):
    """Automatically uses scan file if available, otherwise falls back to indicators"""
    from src.visualization.subcharts import CURRENT_SCAN_FILE
    
    try:
        chart_index = KEY_MAPPINGS[key]
        chart = charts[chart_index]
        current_ticker = chart.topbar['ticker'].value
        timeframe = chart.topbar['timeframe'].value
        
        # Auto-detect source
        if CURRENT_SCAN_FILE and CURRENT_SCAN_FILE.exists():
            try:
                scanner_df = pd.read_csv(CURRENT_SCAN_FILE)
                scanner_df = scanner_df[(scanner_df['Ticker'].notna())]
                available_tickers = sorted(scanner_df[
                    scanner_df['Timeframe'] == timeframe
                ]['Ticker'].unique())
                
                if not available_tickers:
                    print("No tickers in scan for this timeframe, using all tickers")
                    available_tickers = sorted(list({
                        f.name.split('_')[0] for f in 
                        Path("data/indicators").glob(f"*_{timeframe}_*.csv")
                    }))
            except Exception as e:
                print(f"Error reading scan file: {e}, falling back to all tickers")
                available_tickers = sorted(list({
                    f.name.split('_')[0] for f in 
                    Path("data/indicators").glob(f"*_{timeframe}_*.csv")
                }))
        else:
            available_tickers = sorted(list({
                f.name.split('_')[0] for f in 
                Path("data/indicators").glob(f"*_{timeframe}_*.csv")
            }))

        if not available_tickers:
            print(f"No tickers available for {timeframe} timeframe")
            return

        try:
            current_index = available_tickers.index(current_ticker)
            next_index = (current_index + 1) % len(available_tickers)
        except ValueError:
            next_index = 0
        
        next_ticker = available_tickers[next_index]
        indicator_file = next(Path("data/indicators").glob(f"{next_ticker}_{timeframe}_*.csv"), None)
        if not indicator_file:
            print(f"No indicator data found for {next_ticker} {timeframe}")
            return
            
        df = pd.read_csv(indicator_file).rename(columns={
            'Open': 'open',
            'Close': 'close',
            'Low': 'low', 
            'High': 'high'
        })
        df.attrs = {'timeframe': timeframe, 'ticker': next_ticker}
        
        for line in chart.lines(): line.set(pd.DataFrame())
        chart.clear_markers()
        prepared_df, _ = prepare_dataframe(df, show_volume)
        configure_base_chart(prepared_df, chart, show_volume, show_banker_RSI)
        add_ui_elements(chart, charts, next_ticker, timeframe, show_volume, show_banker_RSI)
        add_visualizations(chart, prepared_df, False)
        chart.set(prepared_df)
        chart.fit()
        
        print(f"  Loaded {next_ticker} ({timeframe}) from {indicator_file.name}")

    except Exception as e:
        print(f"Error during ticker cycling: {str(e)}")

def _maximize_minimize_hotkey(charts, key):
    if key == ' ':
        default_chart_dimensions = _get_default_chart_dimensions()
        for chart, (width, height) in zip(charts, default_chart_dimensions[len(charts)]):
            chart.resize(width, height)
            chart.fit()
        for chart in charts:
            try: chart.topbar['max'].set('FULLSCREEN') 
            except KeyError: pass
    elif key in ('1','2','3','4'):
        idx = int(key) - 1
        for i, chart in enumerate(charts):
            width, height = (1.0, 1.0) if i == idx else (0.0, 0.0)
            chart.resize(width, height)
            chart.fit()
            try: chart.topbar['max'].set('MINIMIZE' if i == idx else 'FULLSCREEN')
            except KeyError: pass

def _maximize_minimize_button(target_chart, charts):
    button = target_chart.topbar['max']
    if button.value == 'MINIMIZE':
        default_chart_dimensions = _get_default_chart_dimensions()
        for chart, (width, height) in zip(charts, default_chart_dimensions[len(charts)]):
            chart.resize(width, height)
            chart.fit()
        button.set('FULLSCREEN')
    else:
        for chart in charts:
            width, height = (1.0, 1.0) if chart == target_chart else (0.0, 0.0)
            chart.resize(width, height)
            chart.fit()
        button.set('MINIMIZE')

def _get_default_chart_dimensions():
    return {
        1: [(1.0, 1.0)],
        2: [(0.5, 1.0), (0.5, 1.0)],
        3: [(1.0, 0.5), (0.5, 0.5), (0.5, 0.5)],
        4: [(0.5, 0.5)] * 4
    }

def _on_search(chart, input_ticker):
    print(f"Searching for ticker: {input_ticker}")
    try:
        current_timeframe = chart.topbar['timeframe'].value
        matching_files = sorted(INDICATORS_DIR.glob(f"{input_ticker}_{current_timeframe}_*.csv"), reverse=True)
        if not matching_files:
            print(f"No {current_timeframe} data found for {input_ticker}")
            return
        
        selected_file = matching_files[0]
        print(f"Loading data from: {selected_file}")
        
        try:
            df = pd.read_csv(selected_file)
            df = df.rename(columns={'Open':'open','Close':'close','Low':'low','High':'high'}).copy()
            df.attrs['timeframe'] = current_timeframe
            
            lines = chart.lines()
            for line in lines: line.hide_data()
            chart.clear_markers()
            configure_base_chart(df, chart)
            add_ui_elements(chart, [chart], input_ticker, current_timeframe)
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

def _load_timeframe_csv(charts, key, show_volume=False, show_banker_RSI=False):
    chart = charts[int(key)-6]
    ticker = chart.topbar['ticker'].value
    current_timeframe = chart.topbar['timeframe'].value
    timeframe_order = ['weekly','daily','4hour','1hour','30min','15min','5min','1min']
    available_timeframes = []
    for tf in timeframe_order:
        if list(INDICATORS_DIR.glob(f"{ticker}_{tf}_*.csv")):
            available_timeframes.append(tf)
    
    if not available_timeframes:
        print(f"No timeframe data found for {ticker}")
        return

    try:
        current_index = available_timeframes.index(current_timeframe)
    except ValueError:
        current_index = -1
    
    next_index = (current_index + 1) % len(available_timeframes)
    next_timeframe = available_timeframes[next_index]
    matching_files = sorted(INDICATORS_DIR.glob(f"{ticker}_{next_timeframe}_*.csv"), reverse=True)
    selected_file = matching_files[0]
    print(f"Loading {ticker} {next_timeframe} data from: {selected_file}")
    
    df = pd.read_csv(selected_file).rename(columns={'Open':'open','Close':'close','Low':'low','High':'high'}).copy()
    df.attrs['timeframe'] = next_timeframe
    
    lines = chart.lines()
    for line in lines: line.set(pd.DataFrame())
    chart.clear_markers()
    configure_base_chart(df, chart, show_volume, show_banker_RSI)
    add_ui_elements(chart, [chart], ticker, next_timeframe, show_volume, show_banker_RSI)
    add_visualizations(chart, df, False)
    chart.set(df)
    chart.fit()

def get_most_recent_scanner_file():
    scanner_path = INDICATORS_DIR.parent / "scanner"
    if not scanner_path.exists():
        return None
    scan_files = sorted(scanner_path.glob("scan_results_*.csv"), key=lambda x: x.stem.split('_')[-1], reverse=True)
    return scan_files[0] if scan_files else None

def find_indicator_file(ticker, timeframe):
    files = sorted(INDICATORS_DIR.glob(f"{ticker}_{timeframe}_*.csv"), reverse=True)
    return files[0] if files else None

SCREENSHOT_KEY_MAPPINGS = {'_':0,'+':1,'{':2,'}':3}

def _take_screenshot(charts, key, screenshot_dir=None):
    try:
        chart_index = SCREENSHOT_KEY_MAPPINGS[key]
        chart = charts[chart_index]
    except (KeyError, IndexError) as e:
        print(f"Invalid key or chart index: {e}")
        return
    
    if screenshot_dir is None:
        screenshot_dir = Path.cwd() / 'data' / 'screenshots'
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    ticker = chart.topbar['ticker'].value
    timeframe = chart.topbar['timeframe'].value
    timestamp = datetime.now().strftime('%d%m%y_%H%M%S')
    filename = f"{ticker}_{timeframe}_{timestamp}.png"
    filepath = screenshot_dir / filename
    
    try:
        img = chart.screenshot()
        with open(filepath, 'wb') as f:
            f.write(img)
        print(f"Screenshot saved to: {filepath}")
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
