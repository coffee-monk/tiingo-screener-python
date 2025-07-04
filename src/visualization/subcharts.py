import pandas as pd
from pathlib import Path
from src.visualization.src.indicators import add_visualizations
from src.visualization.src.charts import (
    get_charts,
    prepare_dataframe, 
    configure_base_chart, 
    add_ui_elements
)

# Global variable to track active scan file
CURRENT_SCAN_FILE = None
PROJECT_ROOT = Path(__file__).parent.parent.parent
SCANNER_DIR = PROJECT_ROOT / "data" / "scanner"
INDICATOR_DIR = PROJECT_ROOT / "data" / "indicators"

def _get_latest_scan():
    """Get newest scan file in scanner directory"""
    files = sorted(SCANNER_DIR.glob("scan_results_*.csv"), 
                 key=lambda f: f.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError("No scan files found in data/scanner/")
    return files[0]

def _load_scan_data(scan_file):
    """Load scan file with automatic path handling"""
    # Convert to Path and prepend scanner directory if needed
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

def subcharts(
    df_list=None,
    ticker='',
    show_volume=False,
    show_banker_RSI=True,
    scan_file=None,
):
    """
    Visualize data with automatic scan file path handling.
    Usage:
    - subcharts(scan_file='filename.csv')  # Auto-finds in data/scanner/
    - subcharts()  # Loads latest scan
    - subcharts([df1, df2])  # Manual mode
    """
    global CURRENT_SCAN_FILE
    
    # Mode 1: Manual DataFrames
    if df_list is not None:
        dfs = df_list
        CURRENT_SCAN_FILE = None
    
    # Mode 2/3: Scan File Loading
    else:
        # Handle scan file path
        if scan_file:
            if not isinstance(scan_file, Path):
                scan_file = SCANNER_DIR / scan_file
        else:
            scan_file = _get_latest_scan()
        
        print(f"📊 Loading scan: {scan_file.name}")
        CURRENT_SCAN_FILE = scan_file
        
        # Load and validate data
        scan_df = _load_scan_data(scan_file)
        first_valid = scan_df.iloc[0]
        ticker, timeframe = first_valid['Ticker'], first_valid['Timeframe']
        
        # Load indicator data
        indicator_file = next(INDICATOR_DIR.glob(f"{ticker}_{timeframe}_*.csv"), None)
        if not indicator_file:
            raise FileNotFoundError(f"No indicator data for {ticker} {timeframe}")
            
        df = pd.read_csv(indicator_file).rename(columns={
            'Open': 'open', 'Close': 'close', 'Low': 'low', 'High': 'high'
        })
        df.attrs = {'timeframe': timeframe, 'ticker': ticker}
        dfs = [df]

    # Initialize charts
    main_chart, charts = get_charts(dfs)
    
    # Ensure chart names exist
    for i, chart in enumerate(charts):
        chart.name = str(i)
    
    # Configure each chart
    for i, (df, chart) in enumerate(zip(dfs, charts)):
        prepared_df, timeframe = prepare_dataframe(df, show_volume)
        configure_base_chart(prepared_df, chart)
        add_ui_elements(
            chart, 
            charts, 
            df.attrs.get('ticker', ticker),
            timeframe,
            # 'scanner' if CURRENT_SCAN_FILE is not None else None,
            show_volume
        )
        add_visualizations(chart, prepared_df, show_banker_RSI)
        chart.set(prepared_df)
    
    main_chart.show(block=True)
