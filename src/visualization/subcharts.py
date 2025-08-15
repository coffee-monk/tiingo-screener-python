import pandas as pd
from pathlib import Path
from src.visualization.src.indicator_visualizations import add_visualizations
from config.settings import SCANNER_DIR, INDICATORS_DIR
from src.visualization.src.charts import (
    get_charts,
    prepare_dataframe, 
    configure_base_chart, 
    add_ui_elements
)

CURRENT_SCAN_FILE = None

def _get_latest_scan():
    """Get newest scan file in scanner directory"""
    files = sorted(SCANNER_DIR.glob("scan_results_*.csv"), 
                 key=lambda f: f.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError("\nNo scan files found in data/scans/\n")
    return files[0]

def _load_scan_data(scan_file):
    """Load scan file with automatic path handling"""
    scan_path = Path(scan_file)
    if not scan_path.is_absolute() and not scan_path.parent.name == "scanner":
        scan_path = SCANNER_DIR / scan_path.name
    
    if not scan_path.exists():
        raise FileNotFoundError(f"Scan file not found at: {scan_path}")
    
    df = pd.read_csv(scan_path)
    required_cols = {'Ticker', 'Timeframe', 'Open', 'High', 'Low', 'Close'}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in scan file: {missing}")
    
    return df

def _load_indicator_data(ticker, timeframe=None):
    """Load indicator data for specified ticker"""
    # If timeframe not specified, find first available
    if not timeframe:
        indicator_files = sorted(INDICATORS_DIR.glob(f"{ticker}_*.csv"))
        if not indicator_files:
            raise FileNotFoundError(f"No indicator files found for {ticker}")
        indicator_file = indicator_files[0]
        timeframe = indicator_file.stem.split('_')[1]
    else:
        indicator_file = next(INDICATORS_DIR.glob(f"{ticker}_{timeframe}_*.csv"), None)
        if not indicator_file:
            raise FileNotFoundError(f"No indicator data for {ticker} {timeframe}")

    df = pd.read_csv(indicator_file).rename(columns={
        'Open': 'open', 'Close': 'close', 'Low': 'low', 'High': 'high'
    })
    df.attrs = {'timeframe': timeframe, 'ticker': ticker}
    return df

def subcharts(
    df_list=None,
    ticker='',
    show_volume=True,
    show_banker_RSI=False,
    scan_file=None,
):
    """
    Visualize data with prioritized loading:
    1. Manual DataFrames (df_list)
    2. Specified scan file (scan_file)
    3. Specified ticker (ticker)
    4. First available indicator file
    
    Usage:
    - subcharts([df1, df2])  # Manual DataFrames
    - subcharts(scan_file='scan.csv')  # Specific scan file
    - subcharts(ticker='AAPL')  # Specific ticker
    - subcharts()  # First available indicator
    """
    global CURRENT_SCAN_FILE
    
    # Mode 1: Manual DataFrames
    if df_list is not None:
        dfs = df_list
        CURRENT_SCAN_FILE = None
        print("\n  📊 Using manually provided DataFrame(s)")
    
    else:
        # Mode 2: Scan File Specified
        if scan_file:
            scan_path = Path(scan_file) if isinstance(scan_file, Path) else SCANNER_DIR / scan_file
            print(f"\n  📊 Loading scan: {scan_path.name}\n")
            
            scan_df = _load_scan_data(scan_path)
            first_valid = scan_df.iloc[0]
            ticker, timeframe = first_valid['Ticker'], first_valid['Timeframe']
            CURRENT_SCAN_FILE = scan_path
            
            df = _load_indicator_data(ticker, timeframe)
            dfs = [df]
        
        # Mode 3: Ticker Specified
        elif ticker:
            print(f"📊 Loading data for {ticker}")
            CURRENT_SCAN_FILE = None
            df = _load_indicator_data(ticker)
            dfs = [df]
        
        # Mode 4: Default - First Indicator File
        else:
            indicator_files = sorted(INDICATORS_DIR.glob("*_*_*.csv"))
            if not indicator_files:
                raise FileNotFoundError("No indicator files found in indicators directory")
            
            indicator_file = indicator_files[0]
            print(f"📊 Loading first available indicator: {indicator_file.name}")
            
            ticker, timeframe = indicator_file.stem.split('_')[:2]
            CURRENT_SCAN_FILE = None
            df = _load_indicator_data(ticker, timeframe)
            dfs = [df]

    # Initialize and configure charts
    main_chart, charts = get_charts(dfs)
    
    for i, chart in enumerate(charts):
        chart.name = str(i)
    
    for i, (df, chart) in enumerate(zip(dfs, charts)):
        prepared_df, timeframe = prepare_dataframe(df, show_volume)
        configure_base_chart(prepared_df, chart, show_volume, show_banker_RSI)
        add_ui_elements(
            chart, 
            charts, 
            df.attrs.get('ticker', ticker),
            timeframe,
            show_volume,
            show_banker_RSI,
        )
        add_visualizations(chart, prepared_df, show_banker_RSI)
        chart.set(prepared_df)
    
    main_chart.show(block=True)
