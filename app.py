import os
import argparse
import shutil
import pandas as pd
from pathlib import Path
from datetime import datetime
from src.indicators.get_indicators import get_indicators
from src.indicators.run_indicators import run_indicators
from src.fetch_data.fetch_tickers  import fetch_tickers
from src.fetch_data.fetch_ticker   import fetch_ticker
from src.scanner.scanner           import run_scanner
from src.visualization.subcharts   import subcharts
from src.scanner.custom_inputs     import scan_configs
from src.indicators.custom_inputs  import ind_configs

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

PROJECT_ROOT = Path(__file__).parent
SCANNER_DIR = PROJECT_ROOT / "data" / "scanner"
TICKERS_DIR = PROJECT_ROOT / "data" / "tickers"
INDICATORS_DIR = PROJECT_ROOT / "data" / "indicators"

indicators = ind_configs['indicators']
params = ind_configs['params']

# VISUALIZATION -------------------------------------------

def vis(scan_file=None): 

    if scan_file:

        scan_path = Path(scan_file)
        if not scan_path.exists() and not scan_path.parent.name == "scanner":
            scan_path = SCANNER_DIR / scan_path.name
        
        if not scan_path.exists():
            print(f"Error: Scan file not found at {scan_path}")
            list_scan_files()
            return

        subcharts(scan_file=scan_path, 
                  show_volume=True, show_banker_RSI=False)

    else:

        ticker = 'BTCUSD'

        # df1 = fetch_ticker(timeframe='w', ticker=ticker, api_key=API_KEY)
        df2 = fetch_ticker(timeframe='d', ticker=ticker, api_key=API_KEY)
        # df3 = fetch_ticker(timeframe='h', ticker=ticker, api_key=API_KEY)
        # df4 = fetch_ticker(timeframe='5min', ticker=ticker, api_key=API_KEY)

        # df1 = get_indicators(df1, indicators['weekly'], params['weekly'])
        df2 = get_indicators(df2, indicators['daily'], params['daily'])
        # df3 = get_indicators(df3, indicators['1hour'], params['1hour'])
        # df4 = get_indicators(df4, indicators['5min'], params['5min'])

        subcharts([df2], ticker=ticker, 
                  show_volume=True, show_banker_RSI=False)


def fetch():

    fetch_tickers(['weekly'], api_key=API_KEY)
    fetch_tickers(['daily'],  api_key=API_KEY)
    fetch_tickers(['1hour'],  api_key=API_KEY)
    fetch_tickers(['5min'],   api_key=API_KEY)

# INDICATORS ----------------------------------------------

def ind():

    run_indicators(indicators['weekly'], params['weekly'], "weekly")
    run_indicators(indicators['daily'],  params['daily'],  "daily")
    run_indicators(indicators['1hour'],  params['1hour'],  "1hour")
    run_indicators(indicators['5min'],   params['5min'],   "5min")

# SCANNER -------------------------------------------------

def scan():

    scans = [
             'd_QQEMODOversold_OBSupport',
             'd_bankerRSI_QQEMODOversold',
             'dh_StDevOversold_OBSupport',
             'dh_StDevOverbought_OBResistance',
             'dh_OBSupport',
             'dh_OBResistance',
             'h_StDevOversold_OBSupport',
             'h_OBSupport',
             'h_bankerRSI_QQEMODOversold',
            ]

    for scan in scans:
        kwargs = {
            'criteria': scan_configs[scan]['criteria'],
            'criteria_params': scan_configs[scan]['params'],
            'scan_name': scan
        }
        run_scanner(**kwargs)

def clear_folders():
    """Clear all data folders"""
    folders = [TICKERS_DIR, INDICATORS_DIR, SCANNER_DIR]
    
    for folder in folders:
        if folder.exists():
            for file in folder.glob('*'):
                try:
                    if file.is_file():
                        file.unlink()
                    elif file.is_dir():
                        shutil.rmtree(file)
                except Exception as e:
                    print(f"Error deleting {file}: {e}")
        else:
            folder.mkdir(parents=True, exist_ok=True)
    print("All data folders cleared successfully.")

def list_scan_files():
    """List available scan files with dates"""
    print(SCANNER_DIR)
    scans = sorted(SCANNER_DIR.glob("scan_results_*.csv"), 
                key=lambda f: f.stat().st_mtime, reverse=True)
    if not scans:
        print("No scan files found in data/scanner/")
        return
    
    print("\nAvailable scan files:")
    for i, scan in enumerate(scans[:10]):  # Show 10 most recent
        print(f"{i+1}. {scan.name}")
    print("\nUse with: --vis --scan-file 'filename.csv'")

# FULL RUN (FETCH TICKERS + INDICATORS + SCANNER) ---------

def full_run():
    """Complete pipeline: clear folders, fetch data, generate indicators, run scanner"""
    clear_folders()
    fetch() ; print('=== FETCH TICKERS ===\n')
    ind()   ; print('=== RUN INDICATORS ===\n')
    scan()  ; print('=== RUN SCANNER ===\n')

# COMMAND LINE INTERFACE (CLI) ----------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock Analysis Toolkit")

    # Main commands
    parser.add_argument('--vis', action='store_true', help='Launch visualization')
    parser.add_argument('--fetch', action='store_true', help='Fetch ticker data')
    parser.add_argument('--ind', action='store_true', help='Generate indicators')
    parser.add_argument('--scan', action='store_true', help='Run scanner')
    parser.add_argument('--full-run', action='store_true', 
                        help='Complete pipeline: clear folders, fetch data, generate indicators, run scanner')
    parser.add_argument('--clear-folders', action='store_true', 
                        help='Clear all data folders (tickers, indicators, scanner)')

    # New scan file options
    parser.add_argument('--scan-file', type=str, default=None,
                        help='Specify scan file (e.g. "scan_results_300625.csv")')
    parser.add_argument('--list-scans', action='store_true',
                        help='Show available scan files')

    args = parser.parse_args()

    if   args.list_scans: list_scan_files()
    elif args.vis: vis(scan_file=args.scan_file)
    elif args.fetch: fetch()
    elif args.ind: ind()
    elif args.scan: scan()
    elif args.full_run: full_run()
    elif args.clear_folders: clear_folders()
    else: 
        print("""Available commands:
        --vis                              Launch visualization
        --vis --scan-file "filename.csv"   Visualize specific scan
        --list-scans                       Show available scan files
        --fetch                            Fetch ticker data
        --ind                              Generate indicators
        --scan                             Run scanner
        --full-run                         Reset + Tickers + Indicators + Scanner
        --clear-folders                    Clear data folders""")
