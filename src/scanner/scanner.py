# import os
# import pandas as pd
# from pathlib import Path
# from datetime import datetime
# import importlib
# import requests
#
# PROJECT_ROOT = Path(__file__).parent.parent.parent
# INPUT_DIR = PROJECT_ROOT / "data/indicators"
# OUTPUT_DIR = PROJECT_ROOT / "data/scanner"
# CRITERIA_DIR = PROJECT_ROOT / "scanner/criteria"
# SCAN_DATE = datetime.now().strftime("%d%m%y")
#
# def run_scanner(criteria='banker_RSI', logic='AND', api_key='Tiingo API Key'):
#     """Ultimate flexible scanner with single criteria parameter:
# 
#     1. String:  run_scanner('RSI') → Single criteria all files
#     2. List:    run_scanner(['RSI', 'Volume']) → Multiple criteria all files
#     3. Dict:    run_scanner({'day':'RSI', 'hour':'MACD'}) → Criteria per timeframe
# 
#     Args:
#         criteria: String, List, or Dict of criteria
#         logic: 'AND'/'OR' for dict mode only
#     """
#     print(f"Input directory: {INPUT_DIR}")
#     print(f"Output directory: {OUTPUT_DIR}")
#
#     if isinstance(criteria, dict):
#         return _advanced_scan(criteria, logic, api_key)
#     elif isinstance(criteria, list):
#         return _multi_criteria_scan(criteria, api_key)
#     else:
#         return _simple_scan(criteria, api_key)
#
# def _simple_scan(criteria, api_key='Tiingo API Key'):
#     """Single criteria applied to all files"""
#     criteria_func = _load_criteria(criteria)
#     if not criteria_func:
#         return pd.DataFrame()
#
#     all_results = []
#     for file in _get_data_files():
#         ticker, timeframe = _parse_filename(file)
#         df = _load_indicator_file(INPUT_DIR / file)
#         results = criteria_func(df)
#     
#         if not results.empty:
#             results['Ticker'] = ticker
#             results['Timeframe'] = timeframe
#             all_results.append(results)
# 
#     return _process_results(all_results, f"'{criteria}' scan", api_key)
#
# def _multi_criteria_scan(criteria_list, api_key='Tiingo API Key'):
#     """Multiple criteria (ALL must pass) for all files"""
#     criteria_funcs = [_load_criteria(c) for c in criteria_list]
#     if not all(criteria_funcs):
#         return pd.DataFrame()
#
#     all_results = []
#     for file in _get_data_files():
#         ticker, timeframe = _parse_filename(file)
#         df = _load_indicator_file(INPUT_DIR / file)
#     
#         passed_all = True
#         combined_results = None
#     
#         for criteria_func in criteria_funcs:
#             results = criteria_func(df)
#             if results.empty:
#                 passed_all = False
#                 break
#             
#             if combined_results is None:
#                 combined_results = results.copy()
#             else:
#                 combined_results = combined_results[combined_results.index.isin(results.index)]
#     
#         if passed_all and combined_results is not None:
#             combined_results['Ticker'] = ticker
#             combined_results['Timeframe'] = timeframe
#             all_results.append(combined_results)
# 
#     return _process_results(all_results, f"multi-criteria {criteria_list} scan", api_key)
#
# def _advanced_scan(timeframe_criteria, logic, api_key='Tiingo API Key'):
#     """Criteria applied to specific timeframes. Only passes if ALL timeframes:
#        1. Exist in the data
#        2. Meet their criteria
#     """
#     criteria_funcs = {}
#     for timeframe, criteria_name in timeframe_criteria.items():
#         if isinstance(criteria_name, list):  # Multiple criteria for one timeframe
#             funcs = [_load_criteria(c) for c in criteria_name]
#             if not all(funcs):
#                 return pd.DataFrame()
#             criteria_funcs[timeframe] = funcs
#         else:  # Single criteria
#             func = _load_criteria(criteria_name)
#             if not func:
#                 return pd.DataFrame()
#             criteria_funcs[timeframe] = func
#
#     # Group files by ticker and track available timeframes
#     ticker_files = {}
#     for file in _get_data_files():
#         ticker, timeframe = _parse_filename(file)
#         ticker_files.setdefault(ticker, {})[timeframe] = file
#
#     all_results = []
#     for ticker, files in ticker_files.items():
#         signals = {}
#         results = {}
#         missing_timeframes = []
#
#         # Check for missing timeframes first
#         for timeframe in criteria_funcs.keys():
#             if timeframe not in files:
#                 missing_timeframes.append(timeframe)
#
#         # Skip if any timeframe is missing
#         if missing_timeframes:
#             print(f"Skipping {ticker}: Missing timeframes {missing_timeframes}")
#             continue
#
#         # Now test criteria for all timeframes
#         for timeframe, criteria in criteria_funcs.items():
#             df = _load_indicator_file(INPUT_DIR / files[timeframe])
#
#             if isinstance(criteria, list):  # Multi-criteria for this timeframe
#                 passed_all = True
#                 timeframe_results = None
#
#                 for criteria_func in criteria:
#                     res = criteria_func(df)
#                     if res.empty:
#                         passed_all = False
#                         break
#
#                     if timeframe_results is None:
#                         timeframe_results = res.copy()
#                     else:
#                         timeframe_results = timeframe_results[timeframe_results.index.isin(res.index)]
#
#                 if passed_all and timeframe_results is not None:
#                     timeframe_results['Ticker'] = ticker
#                     timeframe_results['Timeframe'] = timeframe
#                     signals[timeframe] = True
#                     results[timeframe] = timeframe_results
#                 else:
#                     signals[timeframe] = False
#
#             else:  # Single criteria
#                 res = criteria(df)
#                 if not res.empty:
#                     res['Ticker'] = ticker
#                     res['Timeframe'] = timeframe
#                     signals[timeframe] = True
#                     results[timeframe] = res
#                 else:
#                     signals[timeframe] = False
#
#         # Only save if ALL timeframes passed (and none were missing)
#         if all(signals.values()):
#             all_results.extend(results.values())
#
#     return _process_results(all_results, "advanced scan", api_key)
#
# def _load_criteria(criteria_name):
#     """Helper to load criteria function"""
#     try:
#         criteria_module = importlib.import_module(f"src.scanner.criteria.{criteria_name}")
#         return getattr(criteria_module, criteria_name)
#     except Exception as e:
#         print(f"Error loading criteria '{criteria_name}': {str(e)}")
#         return None
#
# def _get_data_files():
#     """Helper to get all data files"""
#     return [f for f in os.listdir(INPUT_DIR) if f.endswith(".csv")]
#
# def _process_results(results, scan_type, api_key='Tiingo API Key'):
#     """Process results with reordered columns (Ticker, Timeframe first, date last)"""
#     if not results:
#         print(f"\nResults: {scan_type} found no setups")
#         return pd.DataFrame()
#   
#     final_results = pd.concat(results)
#   
#     # Create new DataFrame with just the columns we want
#     minimal_results = pd.DataFrame({
#         'Ticker': final_results['Ticker'],
#         'Timeframe': final_results['Timeframe']
#     })
#
#     minimal_results = _attach_fundamentals_to_scanner(minimal_results, api_key)
#
#     _save_scan_results(minimal_results, OUTPUT_DIR, SCAN_DATE)
#     print(f"\nResults: {scan_type} found {len(minimal_results)} setups")
#     return minimal_results
#
# def _save_scan_results(df, output_dir, scan_date):
#     """Save with reordered columns and no index"""
#     filename = f"scan_results_{scan_date}.csv"
#     filepath = output_dir / filename
#     df.to_csv(filepath, index=False)  # No additional index column
#
# def _parse_filename(filename):
#     parts = filename.split("_")
#     return parts[0], parts[1]
#
# def _load_indicator_file(filepath):
#     df = pd.read_csv(filepath, parse_dates=['date'], index_col='date')
#     return df
#
# def _save_scan_results(df, output_dir, scan_date):
#     filename = f"scan_results_{scan_date}.csv"
#     filepath = output_dir / filename
#     df.to_csv(filepath, index=True, index_label='date')
#
# # def _attach_fundamentals_to_scanner(scanner_df, api_key):
# #     """
# #     Simplified version that:
# #     1. Gets latest fundamentals for each ticker
# #     2. Merges all fundamental metrics in one operation
# #     3. Preserves error handling
# #     """
# #     if 'Ticker' not in scanner_df.columns:
# #         return scanner_df
# #
# #     # Define the fundamental metrics we want to fetch
# #     fundamental_metrics = [
# #         'marketCap', 
# #         'enterpriseVal', 
# #         'peRatio',
# #         'pbRatio', 
# #         'trailingPEG1Y'
# #     ]
# #
# #     # Create a DataFrame to store all fundamentals
# #     fundamentals = pd.DataFrame(index=scanner_df['Ticker'].unique())
# #
# #     # Fetch data for each ticker
# #     for ticker in fundamentals.index:
# #         try:
# #             response = requests.get(
# #                 f"https://api.tiingo.com/tiingo/fundamentals/{ticker}/daily?token={api_key}",
# #                 headers={'Content-Type': 'application/json'}
# #             )
# #             response.raise_for_status()
# #            
# #             if fund_data := response.json():
# #                 # Get most recent data point
# #                 latest = pd.DataFrame(fund_data).iloc[-1]
# #                 # Store all requested metrics
# #                 for metric in fundamental_metrics:
# #                     fundamentals.loc[ticker, metric] = latest.get(metric)
# #             else:
# #                 print(f"No data found for {ticker}")
# #                
# #         except Exception as e:
# #             print(f"Error fetching {ticker}: {str(e)}")
# #
# #     # Merge fundamentals with scanner data
# #     for metric in fundamental_metrics:
# #         scanner_df[metric] = scanner_df['Ticker'].map(fundamentals[metric])
# #
# #     return scanner_df
#
# # def _attach_fundamentals_to_scanner(scanner_df, api_key):
# #     """
# #     Final optimized version with:
# #     1. Human-readable formatting
# #     2. Clean CSV output (empty values instead of N/A)
# #     3. Original column names only
# #     4. Preserved precision for calculations
# #     """
# #     if 'Ticker' not in scanner_df.columns:
# #         return scanner_df
# #
# #     # Configuration for number formatting
# #     format_config = {
# #         'marketCap': {'format': '${:,.2f}B', 'divisor': 1e9},
# #         'enterpriseVal': {'format': '${:,.2f}B', 'divisor': 1e9},
# #         'peRatio': {'format': '{:.2f}', 'divisor': 1},
# #         'pbRatio': {'format': '{:.2f}', 'divisor': 1},
# #         'trailingPEG1Y': {'format': '{:.2f}', 'divisor': 1}
# #     }
# #
# #     # Fetch fundamentals data
# #     fundamentals = {}
# #     for ticker in scanner_df['Ticker'].unique():
# #         try:
# #             response = requests.get(
# #                 f"https://api.tiingo.com/tiingo/fundamentals/{ticker}/daily?token={api_key}",
# #                 headers={'Content-Type': 'application/json'}
# #             )
# #             response.raise_for_status()
# #             if fund_data := response.json():
# #                 latest = pd.DataFrame(fund_data).iloc[-1]
# #                 fundamentals[ticker] = latest.to_dict()
# #         except Exception as e:
# #             print(f"Error fetching {ticker}: {str(e)}")
# #
# #     # Apply formatting directly to original columns
# #     for metric, config in format_config.items():
# #         if metric in fundamentals.get(next(iter(fundamentals), {}):
# #             # Store original values
# #             scanner_df[metric] = scanner_df['Ticker'].map(
# #                 lambda x: fundamentals.get(x, {}).get(metric)
# #            
# #             # Format display values
# #             scanner_df[metric] = scanner_df[metric].apply(
# #                 lambda x: config['format'].format(x/config['divisor']) 
# #                 if pd.notnull(x) else None
# #             )
# #
# #     return scanner_df
#
#
#
#
# def _attach_fundamentals_to_scanner(scanner_df, api_key):
#     """
#     Attaches fundamentals data to scanner DataFrame with:
#     - Human-readable formatting
#     - Empty values for missing data
#     - Original column names only
#     - Single API call per ticker
#     """
#     if 'Ticker' not in scanner_df.columns:
#         return scanner_df
#
#     # Configuration for number formatting
#     format_config = {
#         'marketCap': {'format': '${:,.2f}B', 'divisor': 1e9},
#         'enterpriseVal': {'format': '${:,.2f}B', 'divisor': 1e9},
#         'peRatio': {'format': '{:.2f}', 'divisor': 1},
#         'pbRatio': {'format': '{:.2f}', 'divisor': 1},
#         'trailingPEG1Y': {'format': '{:.2f}', 'divisor': 1}
#     }
#
#     # Fetch fundamentals for all unique tickers
#     fundamentals = {}
#     for ticker in scanner_df['Ticker'].unique():
#         try:
#             response = requests.get(
#                 f"https://api.tiingo.com/tiingo/fundamentals/{ticker}/daily?token={api_key}",
#                 headers={'Content-Type': 'application/json'},
#                 timeout=10
#             )
#             response.raise_for_status()
#             fund_data = response.json()
#           
#             if fund_data:
#                 latest = pd.DataFrame(fund_data).iloc[-1]
#                 fundamentals[ticker] = {
#                     metric: latest.get(metric) 
#                     for metric in format_config.keys()
#                 }
#         except Exception as e:
#             print(f"Error fetching {ticker}: {str(e)}")
#             continue
#
#     # Apply formatting to each metric
#     for metric, config in format_config.items():
#         # Create series with original values
#         values = scanner_df['Ticker'].map(
#             lambda x: fundamentals.get(x, {}).get(metric)
#         )
#       
#         # Format non-null values
#         scanner_df[metric] = values.apply(
#             lambda x: config['format'].format(x/config['divisor']) 
#             if pd.notnull(x) else None
#         )
#
#     return scanner_df







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

def run_scanner(criteria='banker_RSI', logic='AND', api_key='Tiingo API Key'):
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
        return _advanced_scan(criteria, logic, api_key)
    elif isinstance(criteria, list):
        return _multi_criteria_scan(criteria, api_key)
    else:
        return _simple_scan(criteria, api_key)

def _simple_scan(criteria, api_key='Tiingo API Key'):
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

def _multi_criteria_scan(criteria_list, api_key='Tiingo API Key'):
    """Flexible multi-criteria scanner that works with ANY criteria functions"""
    criteria_funcs = [_load_criteria(c) for c in criteria_list]
    if not all(criteria_funcs):
        return pd.DataFrame()

    all_results = []
    for file in _get_data_files():
        ticker, timeframe = _parse_filename(file)
        df = _load_indicator_file(INPUT_DIR / file)
       
        # Check ALL criteria pass for this stock
        passed = True
        criteria_data = {}  # Store results from each criteria
       
        for criteria_func in criteria_funcs:
            result = criteria_func(df)
            if result.empty:
                passed = False
                break
            criteria_data[criteria_func.__name__] = result.iloc[-1].to_dict()
       
        if passed:
            # Create result row with metadata and all criteria values
            result_row = {
                'Ticker': ticker,
                'Timeframe': timeframe,
                'Close': df.iloc[-1]['Close'],
                'Timestamp': df.index[-1]
            }
            # Add all criteria outputs
            result_row.update(criteria_data)
            all_results.append(pd.DataFrame(result_row, index=[0]))
   
    return _process_results(all_results if all_results else [], 
                          f"multi-criteria {criteria_list} scan", 
                          api_key)

def _advanced_scan(timeframe_criteria, logic, api_key='Tiingo API Key'):
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

    return _process_results(all_results, "advanced scan", api_key)

def _load_criteria(criteria_name):
    """Helper to load criteria function with fixed import path"""
    try:
        # Updated import path to match your project structure
        criteria_module = importlib.import_module(f"src.scanner.criteria.{criteria_name}")
        return getattr(criteria_module, criteria_name)
    except Exception as e:
        print(f"Error loading criteria '{criteria_name}': {str(e)}")
        return None

def _get_data_files():
    """Helper to get all data files"""
    return [f for f in os.listdir(INPUT_DIR) if f.endswith(".csv")]

def _process_results(results, scan_type, api_key='Tiingo API Key'):
    """Process results with reordered columns (Ticker, Timeframe first)"""
    if not results or len(results) == 0:  # Proper empty check
        print(f"\nResults: {scan_type} found no setups")
        return pd.DataFrame()
   
    try:
        final_results = pd.concat(results)
    except ValueError:  # If all DataFrames are empty
        print(f"\nResults: {scan_type} found no setups")
        return pd.DataFrame()
   
    # Create new DataFrame with standard columns
    minimal_results = pd.DataFrame({
        'Ticker': final_results['Ticker'],
        'Timeframe': final_results['Timeframe'],
        'Close': final_results['Close'],
        'Timestamp': final_results['Timestamp']
    })

    # Add all criteria-specific columns
    for col in final_results.columns:
        if col not in minimal_results.columns:
            minimal_results[col] = final_results[col]

    minimal_results = _attach_fundamentals_to_scanner(minimal_results, api_key)

    _save_scan_results(minimal_results, OUTPUT_DIR, SCAN_DATE)
    print(f"\nResults: {scan_type} found {len(minimal_results)} setups")
    return minimal_results

def _save_scan_results(df, output_dir, scan_date):
    """Save with reordered columns and no index"""
    filename = f"scan_results_{scan_date}.csv"
    filepath = output_dir / filename
    df.to_csv(filepath, index=False)

def _parse_filename(filename):
    parts = filename.split("_")
    return parts[0], parts[1]

def _load_indicator_file(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'], index_col='date')
    return df

def _attach_fundamentals_to_scanner(scanner_df, api_key):
    """
    Attaches fundamentals data to scanner DataFrame with:
    - Human-readable formatting
    - Empty values for missing data
    - Single API call per ticker
    """
    if 'Ticker' not in scanner_df.columns:
        return scanner_df

    # Configuration for number formatting
    format_config = {
        'marketCap': {'format': '${:,.2f}B', 'divisor': 1e9},
        'enterpriseVal': {'format': '${:,.2f}B', 'divisor': 1e9},
        'peRatio': {'format': '{:.2f}', 'divisor': 1},
        'pbRatio': {'format': '{:.2f}', 'divisor': 1},
        'trailingPEG1Y': {'format': '{:.2f}', 'divisor': 1}
    }

    # Fetch fundamentals for all unique tickers
    fundamentals = {}
    for ticker in scanner_df['Ticker'].unique():
        try:
            response = requests.get(
                f"https://api.tiingo.com/tiingo/fundamentals/{ticker}/daily?token={api_key}",
                headers={'Content-Type': 'application/json'},
                timeout=10
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

    # Apply formatting to each metric
    for metric, config in format_config.items():
        # Create series with original values
        values = scanner_df['Ticker'].map(lambda x: fundamentals.get(x, {}).get(metric))
       
        # Format non-null values
        scanner_df[metric] = values.apply(
            lambda x: config['format'].format(x/config['divisor']) if pd.notnull(x) else None
        )

    return scanner_df





