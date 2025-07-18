import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import importlib
import requests
from config.settings import SCANNER_DIR, INDICATORS_DIR, DATE_STAMP

def run_scanner(criteria='banker_RSI', criteria_params=None, logic='AND', api_key=None, scan_name=None):
    """Ultimate flexible scanner with support for criteria parameters.

    Args:
        criteria: String, List, or Dict of criteria
        logic: 'AND'/'OR' for dict mode only
        api_key: Optional Tiingo API key
        criteria_params: Dict of parameter dicts for criteria functions
        scan_name: Optional custom name suffix for output file

    Syntax Examples:
        run_scanner('TTM_squeeze')
        run_scanner(['QQEMOD_overbought', 'StDev'])
        run_scanner(
                    criteria={ 
                     # 'weekly': ['TTM_squeeze'], 
                     'daily':  ['StDev'],
                     # '1hour': ['OB_support'], 
                     # '5min': ['SMA_above'], 
                    }, 
                    logic='AND',
                    criteria_params={
                        'StDev': {
                            'daily': {
                                'threshold': 2,
                                'mode': 'overbought'
                                }
                            }
                        }
                   )
    """
    print('\n=== SCANNER ===\n')
    print(f"Input directory: {INDICATORS_DIR}")
    print(f"Output directory: {SCANNER_DIR}")

    # Initialize empty params if none provided
    if criteria_params is None:
        criteria_params = {}

    if isinstance(criteria, dict):
        return _advanced_scan(criteria, logic, api_key, criteria_params, scan_name)
    elif isinstance(criteria, list):
        return _multi_criteria_scan(criteria, api_key, criteria_params, scan_name)
    else:
        return _simple_scan(criteria, api_key, criteria_params, scan_name)

def _simple_scan(criteria, api_key=None, criteria_params=None, scan_name=None):
    """Single criteria applied to all files with optional parameters"""
    criteria_func = _load_criteria(criteria)
    if not criteria_func:
        return pd.DataFrame()

    # Get parameters for this criteria if they exist
    params = criteria_params.get(criteria, {})

    all_results = []
    for file in _get_data_files():
        ticker, timeframe = _parse_filename(file)
        df = _load_indicator_file(INDICATORS_DIR / file)
        
        # Pass parameters to criteria function if it accepts them
        try:
            results = criteria_func(df, **params)
        except TypeError:
            # Fallback to no parameters if function doesn't accept them
            results = criteria_func(df)
      
        if not results.empty:
            results['Ticker'] = ticker
            results['Timeframe'] = timeframe
            all_results.append(results)
  
    return _process_results(all_results, f"'{criteria}' scan", api_key, scan_name)

def _multi_criteria_scan(criteria_list, api_key=None, criteria_params=None, scan_name=None):
    """Multiple criteria (ALL must pass) for all files with parameters"""
    criteria_funcs = [_load_criteria(c) for c in criteria_list]
    if not all(criteria_funcs):
        return pd.DataFrame()

    all_results = []
    for file in _get_data_files():
        ticker, timeframe = _parse_filename(file)
        df = _load_indicator_file(INDICATORS_DIR / file)
        
        # Check ALL criteria pass for this stock
        passed = True
        criteria_data = {}
        
        for criteria_func in criteria_funcs:
            # Get parameters for this criteria if they exist
            func_name = criteria_func.__name__
            params = criteria_params.get(func_name, {})
            
            try:
                result = criteria_func(df, **params)
            except TypeError:
                # Fallback to no parameters if function doesn't accept them
                result = criteria_func(df)
                
            if result.empty:
                passed = False
                break
            criteria_data[func_name] = result.iloc[-1].to_dict()
        
        if passed:
            result_row = {
                'date': df.index[-1],
                'Ticker': ticker,
                'Timeframe': timeframe,
                'Close': df.iloc[-1]['Close']
            }
            result_row.update(criteria_data)
            all_results.append(pd.DataFrame(result_row, index=[0]))
    
    return _process_results(all_results, f"multi-criteria {criteria_list} scan", api_key, scan_name)

def _advanced_scan(timeframe_criteria, logic='AND', api_key=None, criteria_params=None, scan_name=None):
    """Enhanced timeframe scanner with parameter support"""
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
            df = _load_indicator_file(INDICATORS_DIR / files[timeframe])
            
            passed_all = True
            for criteria_func in criteria_funcs:
                # Get parameters for this criteria if they exist
                func_name = criteria_func.__name__
                
                # Check for timeframe-specific parameters first
                timeframe_params = {}
                if func_name in criteria_params:
                    if timeframe in criteria_params[func_name]:
                        timeframe_params = criteria_params[func_name][timeframe]
                    elif isinstance(criteria_params[func_name], dict):
                        # Use general params if no timeframe-specific ones exist
                        timeframe_params = criteria_params[func_name]
                
                try:
                    results = criteria_func(df, **timeframe_params)
                except TypeError:
                    # Fallback to no parameters if function doesn't accept them
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
            # Combine all passing timeframes
            combined = pd.concat([timeframe_results[tf] for tf in timeframe_signals if timeframe_signals[tf]])
            
            # Create single result row with all passing timeframes noted
            result_row = {
                'date': combined.iloc[0]['date'],
                'Ticker': ticker,
                'Timeframe': '|'.join([tf for tf, passed in timeframe_signals.items() if passed]),
                'Close': combined.iloc[0]['Close']
            }
            
            # Add criteria data from all passing timeframes
            for tf, passed in timeframe_signals.items():
                if passed:
                    for col in timeframe_results[tf].columns:
                        if col not in ['date', 'Ticker', 'Timeframe', 'Close']:
                            result_row[f'{tf}_{col}'] = timeframe_results[tf][col].iloc[0]
            
            all_results.append(pd.DataFrame(result_row, index=[0]))

    return _process_results(all_results, "advanced scan", api_key, scan_name)

def _load_criteria(criteria_name):
    """Helper to load criteria function from src.scanner.criteria"""
    try:
        criteria_module = importlib.import_module(f"src.scanner.criteria.{criteria_name}")
        return getattr(criteria_module, criteria_name)
    except Exception as e:
        print(f"Error loading criteria '{criteria_name}': {str(e)}")
        return None

def _get_data_files():
    """Get all data files in input directory"""
    return [f for f in os.listdir(INDICATORS_DIR) if f.endswith(".csv")]

def _process_results(results, scan_type, api_key=None, scan_name=None):
    """Process and format results without fragmentation"""
    if not results or len(results) == 0:
        print(f"\nResults: {scan_type} found no setups\n")
        return pd.DataFrame()
    
    try:
        final_results = pd.concat(results)
    except ValueError:
        print(f"\nResults: {scan_type} found no setups\n")
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
    _save_scan_results(minimal_results, SCANNER_DIR, DATE_STAMP, scan_name)
    print(f"\nResults: {scan_type} found {len(minimal_results)} setups\n")
    return minimal_results

def _save_scan_results(df, output_dir, scan_date, scan_name=None):
    """Save scan results to CSV with custom naming"""
    filename = f"scan_results_{scan_date}"
    if scan_name:
        filename += f"_{scan_name}"
    filename += ".csv"
    filepath = output_dir / filename
    df.to_csv(filepath, index=False)
    print(f"Results saved to: {filepath}")

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
