import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from src.visualization.subcharts import subcharts

SUPPORTED_FOLDERS = ["tickers", "indicators", "scanner"]
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "data"

def subcharts_data(ticker: str = "AAPL",
                  data_folder: str = "indicators",  # tickers, indicators, scanner
                  timeframes: Optional[List[str]] = None,
                  show_volume: bool = False):
    """
    Main function to load and visualize ticker data with special scanner handling.
    """
    if data_folder == "scanner":
        # Special handling for scanner files
        scanner_file = get_most_recent_scanner_file()
        if not scanner_file:
            print("No scanner results found")
            return
           
        # Get ticker's timeframes from scanner results
        scanner_dfs = load_scanner_data(scanner_file, ticker)
        if not scanner_dfs:
            print(f"No scanner results found for {ticker}")
            return
           
        # Get corresponding indicator files
        indicator_dfs = []
        for df in scanner_dfs:
            tf = df.attrs['timeframe']
            indicator_file = find_indicator_file(ticker, tf)
            if indicator_file:
                indicator_df = load_single_dataframe(indicator_file)
                indicator_df.attrs['timeframe'] = tf
                indicator_dfs.append(indicator_df)
       
        if not indicator_dfs:
            print("No matching indicator data found")
            return
           
        # Create title with all found timeframes
        timeframes_used = [df.attrs['timeframe'] for df in indicator_dfs]
        subcharts(indicator_dfs, ticker=ticker, show_volume=show_volume)
       
    else:
        # Original handling for tickers/indicators folders
        files = find_ticker_files(ticker, data_folder, timeframes)
        if not files:
            print(f"No data files found for {ticker} in {data_folder}")
            return
           
        dfs = load_dataframes(files)
        if not dfs:
            print("No valid data loaded")
            return
           
        subcharts(dfs, ticker=ticker, show_volume=show_volume)

def get_most_recent_scanner_file() -> Optional[Path]:
    """Find the most recent scanner results file"""
    scanner_path = DATA_ROOT / "scanner"
    if not scanner_path.exists():
        return None
       
    # Get all scan results files and sort by date in filename
    scan_files = sorted(
        scanner_path.glob("scan_results_*.csv"),
        key=lambda x: datetime.strptime(x.stem[-6:], "%d%m%y"),
        reverse=True
    )
    return scan_files[0] if scan_files else None

def load_scanner_data(file: Path, ticker: str) -> List[pd.DataFrame]:
    """
    Load scanner CSV and return DataFrames for specific ticker
    with timeframe stored in attrs
    """
    try:
        df = pd.read_csv(file)
        ticker_dfs = []
       
        # Filter for our ticker and group by timeframe
        ticker_data = df[df['Ticker'] == ticker]
        for timeframe, group in ticker_data.groupby('Timeframe'):
            group_df = group.copy()
            group_df.attrs['timeframe'] = timeframe
            ticker_dfs.append(group_df)
           
        return ticker_dfs
    except Exception as e:
        print(f"Error loading scanner data: {e}")
        return []

def find_indicator_file(ticker: str, timeframe: str) -> Optional[Path]:
    """Find the most recent indicator file for specific ticker/timeframe"""
    indicator_path = DATA_ROOT / "indicators"
    pattern = f"{ticker}_{timeframe}_*.csv"
    files = sorted(indicator_path.glob(pattern), reverse=True)
    return files[0] if files else None

def load_single_dataframe(file: Path) -> pd.DataFrame:
    """Load a single CSV file into DataFrame with attrs"""
    df = pd.read_csv(file)
    df.attrs['filepath'] = str(file)
    return df

def find_ticker_files(ticker: str,
                     folder: str = "tickers", 
                     timeframes: Optional[List[str]] = None) -> List[Path]:
    """
    Find files for the ticker, ensuring unique timeframes with most recent dates.
    Returns max 4 files with unique timeframes (most recent dates prioritized).
    """
    if folder not in SUPPORTED_FOLDERS:
        raise ValueError(f"Unsupported folder. Choose from: {SUPPORTED_FOLDERS}")
   
    folder_path = DATA_ROOT / folder
    if not folder_path.exists():
        raise FileNotFoundError(f"Data folder {folder} not found at {folder_path}")
       
    # Find all matching files
    pattern = f"{ticker}_*.csv"
    all_files = list(folder_path.glob(pattern))
   
    # Parse files into (timeframe, date_str, file) tuples
    parsed_files = []
    for file in all_files:
        try:
            # Example filename: "A_15min_040525.csv" -> ["A", "15min", "040525"]
            parts = file.stem.split('_')
            if len(parts) >= 3:
                timeframe = '_'.join(parts[1:-1])  # Handles multi-word timeframes
                date_str = parts[-1]  # Assuming format like "040525" for April 5 2025
                parsed_files.append((timeframe, date_str, file))
        except:
            continue
   
    # Filter by requested timeframes if specified
    if timeframes:
        parsed_files = [x for x in parsed_files if x[0] in timeframes]
   
    # Group by timeframe and select most recent for each
    timeframe_groups = {}
    for timeframe, date_str, file in parsed_files:
        if timeframe not in timeframe_groups or date_str > timeframe_groups[timeframe][1]:
            timeframe_groups[timeframe] = (file, date_str)
   
    # Get sorted list of most recent files (max 4)
    unique_files = sorted(
        [file for file, _ in timeframe_groups.values()],
        key=lambda x: x.name
    )[:4]
   
    return unique_files

def load_dataframes(files: List[Path]) -> List[pd.DataFrame]:
    """
    Load CSV files into DataFrames with timeframe metadata stored in attrs
    """
    dfs = []
    for file in files:
        try:
            df = pd.read_csv(file)
            # Extract timeframe and store as attribute
            timeframe = "_".join(file.stem.split("_")[1:-1])
            df.attrs['timeframe'] = timeframe  # Store in attributes
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return dfs
