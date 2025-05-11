import os
import pandas as pd
from pathlib import Path
from datetime import datetime
import importlib

PROJECT_ROOT = Path(__file__).parent.parent.parent
INPUT_DIR = PROJECT_ROOT / "data/indicators"
OUTPUT_DIR = PROJECT_ROOT / "data/scanner"
CRITERIA_DIR = PROJECT_ROOT / "scanner/criteria"
SCAN_DATE = datetime.now().strftime("%d%m%y")

def run_scanner(criteria='banker_RSI', logic='AND'):
    """Ultimate flexible scanner with single criteria parameter:
  
    1. String:  run_scanner('RSI') → Single criteria all files
    2. List:    run_scanner(['RSI', 'Volume']) → Multiple criteria all files
    3. Dict:    run_scanner({'day':'RSI', 'hour':'MACD'}) → Criteria per timeframe
  
    Args:
        criteria: String, List, or Dict of criteria
        logic: 'AND'/'OR' for dict mode only
    """
    print(f"Input directory: {INPUT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")

    if isinstance(criteria, dict):
        return _advanced_scan(criteria, logic)
    elif isinstance(criteria, list):
        return _multi_criteria_scan(criteria)
    else:
        return _simple_scan(criteria)

def _simple_scan(criteria):
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
  
    return _process_results(all_results, f"'{criteria}' scan")

def _multi_criteria_scan(criteria_list):
    """Multiple criteria (ALL must pass) for all files"""
    criteria_funcs = [_load_criteria(c) for c in criteria_list]
    if not all(criteria_funcs):
        return pd.DataFrame()

    all_results = []
    for file in _get_data_files():
        ticker, timeframe = _parse_filename(file)
        df = _load_indicator_file(INPUT_DIR / file)
      
        passed_all = True
        combined_results = None
      
        for criteria_func in criteria_funcs:
            results = criteria_func(df)
            if results.empty:
                passed_all = False
                break
              
            if combined_results is None:
                combined_results = results.copy()
            else:
                combined_results = combined_results[combined_results.index.isin(results.index)]
      
        if passed_all and combined_results is not None:
            combined_results['Ticker'] = ticker
            combined_results['Timeframe'] = timeframe
            all_results.append(combined_results)
  
    return _process_results(all_results, f"multi-criteria {criteria_list} scan")

def _advanced_scan(timeframe_criteria, logic):
    """Criteria applied to specific timeframes. Only passes if ALL timeframes:
       1. Exist in the data
       2. Meet their criteria
    """
    criteria_funcs = {}
    for timeframe, criteria_name in timeframe_criteria.items():
        if isinstance(criteria_name, list):  # Multiple criteria for one timeframe
            funcs = [_load_criteria(c) for c in criteria_name]
            if not all(funcs):
                return pd.DataFrame()
            criteria_funcs[timeframe] = funcs
        else:  # Single criteria
            func = _load_criteria(criteria_name)
            if not func:
                return pd.DataFrame()
            criteria_funcs[timeframe] = func

    # Group files by ticker and track available timeframes
    ticker_files = {}
    for file in _get_data_files():
        ticker, timeframe = _parse_filename(file)
        ticker_files.setdefault(ticker, {})[timeframe] = file

    all_results = []
    for ticker, files in ticker_files.items():
        signals = {}
        results = {}
        missing_timeframes = []

        # Check for missing timeframes first
        for timeframe in criteria_funcs.keys():
            if timeframe not in files:
                missing_timeframes.append(timeframe)

        # Skip if any timeframe is missing
        if missing_timeframes:
            print(f"Skipping {ticker}: Missing timeframes {missing_timeframes}")
            continue

        # Now test criteria for all timeframes
        for timeframe, criteria in criteria_funcs.items():
            df = _load_indicator_file(INPUT_DIR / files[timeframe])

            if isinstance(criteria, list):  # Multi-criteria for this timeframe
                passed_all = True
                timeframe_results = None

                for criteria_func in criteria:
                    res = criteria_func(df)
                    if res.empty:
                        passed_all = False
                        break

                    if timeframe_results is None:
                        timeframe_results = res.copy()
                    else:
                        timeframe_results = timeframe_results[timeframe_results.index.isin(res.index)]

                if passed_all and timeframe_results is not None:
                    timeframe_results['Ticker'] = ticker
                    timeframe_results['Timeframe'] = timeframe
                    signals[timeframe] = True
                    results[timeframe] = timeframe_results
                else:
                    signals[timeframe] = False

            else:  # Single criteria
                res = criteria(df)
                if not res.empty:
                    res['Ticker'] = ticker
                    res['Timeframe'] = timeframe
                    signals[timeframe] = True
                    results[timeframe] = res
                else:
                    signals[timeframe] = False

        # Only save if ALL timeframes passed (and none were missing)
        if all(signals.values()):
            all_results.extend(results.values())

    return _process_results(all_results, "advanced scan")

def _load_criteria(criteria_name):
    """Helper to load criteria function"""
    try:
        criteria_module = importlib.import_module(f"src.scanner.criteria.{criteria_name}")
        return getattr(criteria_module, criteria_name)
    except Exception as e:
        print(f"Error loading criteria '{criteria_name}': {str(e)}")
        return None

def _get_data_files():
    """Helper to get all data files"""
    return [f for f in os.listdir(INPUT_DIR) if f.endswith(".csv")]

def _process_results(results, scan_type):
    """Helper to process and save results"""
    if results:
        final_results = pd.concat(results)
        _save_scan_results(final_results, OUTPUT_DIR, SCAN_DATE)
        print(f"\nResults: {scan_type} found {len(final_results)} setups")
        return final_results
    else:
        print(f"\nResults: {scan_type} found no setups")
        return pd.DataFrame()

def _parse_filename(filename):
    parts = filename.split("_")
    return parts[0], parts[1]

def _load_indicator_file(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'], index_col='date')
    return df

def _save_scan_results(df, output_dir, scan_date):
    filename = f"scan_results_{scan_date}.csv"
    filepath = output_dir / filename
    df.to_csv(filepath, index=True, index_label='date')
