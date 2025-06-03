import os
import pandas as pd
from pathlib import Path
from datetime import datetime
import importlib
import requests

PROJECT_ROOT = Path(__file__).parent.parent.parent
INPUT_DIR = PROJECT_ROOT / "data/indicators"
OUTPUT_DIR = PROJECT_ROOT / "data/scanner"
CRITERIA_DIR = PROJECT_ROOT / "scanner/criteria"
SCAN_DATE = datetime.now().strftime("%d%m%y")

def run_scanner(criteria='banker_RSI', logic='AND', api_key=None):
    """Ultimate flexible scanner with single criteria parameter:

    1. String:  run_scanner('RSI') → Single criteria all files
    2. List:    run_scanner(['RSI', 'Volume']) → Multiple criteria all files
    3. Dict:    run_scanner({'day':'RSI', 'hour':'MACD'}) → Criteria per timeframe

    Args:
        criteria: String, List, or Dict of criteria
        logic: 'AND'/'OR' for dict mode only
        api_key: Optional Tiingo API key. If provided, fundamentals data will be fetched
    """
    print(f"Input directory: {INPUT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")

    if isinstance(criteria, dict):
        return _advanced_scan(criteria, logic, api_key)
    elif isinstance(criteria, list):
        return _multi_criteria_scan(criteria, api_key)
    else:
        return _simple_scan(criteria, api_key)

def _simple_scan(criteria, api_key=None):
    """Single criteria applied to all files"""
    criteria_func = _load_criteria(criteria)
    if not criteria_func:
        return pd.DataFrame()

    all_results = []
    for file in _get_data_files():
        ticker, timeframe = _parse_filename(file)
        df = _load_indicator_file(INPUT_DIR / file)
        results = criteria_func(df)
      
        if not results.empty:
            results['Ticker'] = ticker
            results['Timeframe'] = timeframe
            all_results.append(results)
  
    return _process_results(all_results, f"'{criteria}' scan", api_key)

def _multi_criteria_scan(criteria_list, api_key=None):
    """Multiple criteria (ALL must pass) for all files"""
    criteria_funcs = [_load_criteria(c) for c in criteria_list]
    if not all(criteria_funcs):
        return pd.DataFrame()

    all_results = []
    for file in _get_data_files():
        ticker, timeframe = _parse_filename(file)
        df = _load_indicator_file(INPUT_DIR / file)
        
        # Check ALL criteria pass for this stock
        passed = True
        criteria_data = {}
        
        for criteria_func in criteria_funcs:
            result = criteria_func(df)
            if result.empty:
                passed = False
                break
            criteria_data[criteria_func.__name__] = result.iloc[-1].to_dict()
        
        if passed:
            result_row = {
                'date': df.index[-1],
                'Ticker': ticker,
                'Timeframe': timeframe,
                'Close': df.iloc[-1]['Close']
            }
            result_row.update(criteria_data)
            all_results.append(pd.DataFrame(result_row, index=[0]))
    
    return _process_results(all_results, f"multi-criteria {criteria_list} scan", api_key)

def _advanced_scan(timeframe_criteria, logic='AND', api_key=None):

    """Enhanced timeframe scanner with proper multi-timeframe support"""
    # Validate and load criteria functions
    timeframe_configs = {}
    for timeframe, criteria_spec in timeframe_criteria.items():
        if isinstance(criteria_spec, (list, tuple)):
            criteria_list = criteria_spec
        else:
            criteria_list = [criteria_spec]
            
        funcs = [_load_criteria(c) for c in criteria_list]
        if not all(funcs):
            return pd.DataFrame()
        timeframe_configs[timeframe] = funcs

    # Group files by ticker
    ticker_files = {}
    for file in _get_data_files():
        ticker, timeframe = _parse_filename(file)
        ticker_files.setdefault(ticker, {})[timeframe] = file

    all_results = []
    for ticker, files in ticker_files.items():
        timeframe_signals = {}
        timeframe_results = {}
        missing_timeframes = []

        # Check for missing timeframes
        for timeframe in timeframe_configs.keys():
            if timeframe not in files:
                missing_timeframes.append(timeframe)

        if missing_timeframes:
            print(f"Skipping {ticker}: Missing timeframes {missing_timeframes}")
            continue

        # Check criteria for each timeframe
        for timeframe, criteria_funcs in timeframe_configs.items():
            df = _load_indicator_file(INPUT_DIR / files[timeframe])
            
            passed_all = True
            for criteria_func in criteria_funcs:
                results = criteria_func(df)
                if results.empty:
                    passed_all = False
                    break
            
            timeframe_signals[timeframe] = passed_all
            if passed_all:
                # Take the most recent data point
                last_row = df.iloc[[-1]].copy()
                last_row['Ticker'] = ticker
                last_row['Timeframe'] = timeframe
                timeframe_results[timeframe] = last_row

        # Apply logic between timeframes
        if logic == 'AND' and all(timeframe_signals.values()):
            combined = pd.concat(timeframe_results.values())
            all_results.append(combined)
                
        elif logic == 'OR' and any(timeframe_signals.values()):
            for timeframe, passed in timeframe_signals.items():
                if passed:
                    all_results.append(timeframe_results[timeframe])

    return _process_results(all_results, "advanced scan", api_key)

def _load_criteria(criteria_name):
    """Helper to load criteria function"""
    try:
        criteria_module = importlib.import_module(f"src.scanner.criteria.{criteria_name}")
        return getattr(criteria_module, criteria_name)
    except Exception as e:
        print(f"Error loading criteria '{criteria_name}': {str(e)}")
        return None

def _get_data_files():
    """Get all data files in input directory"""
    return [f for f in os.listdir(INPUT_DIR) if f.endswith(".csv")]

def _process_results(results, scan_type, api_key=None):
    """Process and format results without fragmentation"""
    if not results or len(results) == 0:
        print(f"\nResults: {scan_type} found no setups")
        return pd.DataFrame()
    
    try:
        final_results = pd.concat(results)
    except ValueError:
        print(f"\nResults: {scan_type} found no setups")
        return pd.DataFrame()
    
    # Reset index to get date as column if it's in index
    if isinstance(final_results.index, pd.DatetimeIndex):
        final_results = final_results.reset_index()
        if 'index' in final_results.columns:
            final_results = final_results.rename(columns={'index': 'date'})
    
    # Prepare all columns at once
    columns_to_keep = {
        'date': final_results['date'],
        'Ticker': final_results['Ticker'],
        'Timeframe': final_results['Timeframe'],
        'Close': final_results['Close']
    }
    
    # Add criteria-specific columns in one operation
    extra_cols = {
        col: final_results[col] 
        for col in final_results.columns 
        if col not in ['date', 'Ticker', 'Timeframe', 'Close']
    }
    
    # Combine all columns at once
    minimal_results = pd.DataFrame({**columns_to_keep, **extra_cols})
    
    if api_key:
        minimal_results = _attach_fundamentals_to_scanner(minimal_results, api_key)
    _save_scan_results(minimal_results, OUTPUT_DIR, SCAN_DATE)
    print(f"\nResults: {scan_type} found {len(minimal_results)} setups")
    return minimal_results

def _save_scan_results(df, output_dir, scan_date):
    """Save scan results to CSV"""
    filename = f"scan_results_{scan_date}.csv"
    filepath = output_dir / filename
    df.to_csv(filepath, index=False)

def _parse_filename(filename):
    """Extract ticker and timeframe from filename"""
    parts = filename.split("_")
    return parts[0], parts[1]

def _load_indicator_file(filepath):
    """Load indicator file with proper date handling"""
    df = pd.read_csv(filepath, parse_dates=['date'])
    return df.set_index('date')

def _attach_fundamentals_to_scanner(scanner_df, api_key):
    """Optimized fundamentals attachment"""
    if 'Ticker' not in scanner_df.columns:
        return scanner_df

    format_config = {
        'marketCap': {'format': '${:,.2f}B', 'divisor': 1e9},
        'enterpriseVal': {'format': '${:,.2f}B', 'divisor': 1e9},
        'peRatio': {'format': '{:.2f}', 'divisor': 1},
        'pbRatio': {'format': '{:.2f}', 'divisor': 1},
        'trailingPEG1Y': {'format': '{:.2f}', 'divisor': 1}
    }

    fundamentals = {}
    for ticker in scanner_df['Ticker'].unique():
        try:
            response = requests.get(
                f"https://api.tiingo.com/tiingo/fundamentals/{ticker}/daily",
                headers={'Content-Type': 'application/json'},
                params={'token': api_key},
            )
            response.raise_for_status()
            fund_data = response.json()
            
            if fund_data:
                latest = pd.DataFrame(fund_data).iloc[-1]
                fundamentals[ticker] = {
                    metric: latest.get(metric) 
                    for metric in format_config.keys()
                }
        except Exception as e:
            print(f"Error fetching {ticker}: {str(e)}")
            continue

    # Apply all formatting in one operation
    formatted_data = {}
    for metric, config in format_config.items():
        values = scanner_df['Ticker'].map(lambda x: fundamentals.get(x, {}).get(metric))
        formatted_data[metric] = values.apply(
            lambda x: config['format'].format(x/config['divisor']) if pd.notnull(x) else None
        )
    
    return scanner_df.assign(**formatted_data)
