import os
import argparse
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
INDICATORS_DIR = PROJECT_ROOT / "data" / "indicators"

indicators = ind_configs['indicators']
params = ind_configs['params']

# VISUALIZATION ------------------------------------------

def vis(scan_file=None): 

    if scan_file:

        scan_path = Path(scan_file)
        if not scan_path.exists() and not scan_path.parent.name == "scanner":
            scan_path = SCANNER_DIR / scan_path.name
        
        if not scan_path.exists():
            print(f"Error: Scan file not found at {scan_path}")
            list_scan_files()
            return
            
        subcharts(scan_file=scan_path)

    else:

        ticker = 'SOFI'

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

# FETCH TICKERS -------------------------------------------

def fetch():

    # fetch_tickers(['weekly'], api_key=API_KEY)
    fetch_tickers(['daily'],  api_key=API_KEY)
    # fetch_tickers(['1hour'],  api_key=API_KEY)
    # fetch_tickers(['5min'],   api_key=API_KEY)

# INDICATORS ----------------------------------------------

def ind():

    # run_indicators(indicators['weekly'], params['weekly'], "weekly")
    run_indicators(indicators['daily'],  params['daily'],  "daily")
    # run_indicators(indicators['1hour'],  params['1hour'],  "1hour")
    # run_indicators(indicators['5min'],   params['5min'],   "5min")

# SCANNER -------------------------------------------------

def scan():

    scans = [
             # 'd_QQEMODOversold_OBSupport',
             # 'd_bankerRSI_QQEMODOversold',
             # 'dh_StDevOversold_OBSupport',
             # 'dh_StDevOverbought_OBResistance',
             # 'dh_OBSupport',
             # 'dh_OBResistance',
             # 'h_StDevOversold_OBSupport',
             # 'h_OBSupport',
             # 'h_bankerRSI_QQEMODOversold',
             # 'd_aVWAPavg',
             # 'd_aVWAPavgAbove',
             # 'd_aVWAPavgBelow',
             'd_SMAAbove',
             'd_SMABelow',
            ]

    for scan in scans:
        kwargs = {
            'criteria': scan_configs[scan]['criteria'],
            'criteria_params': scan_configs[scan]['params'],
            'scan_name': scan
        }
        run_scanner(**kwargs)

# FULL RUN (FETCH TICKERS + INDICATORS + SCANNER) ---------

def full_run():
    """Complete pipeline: clear folders, fetch data, generate indicators, run scanner"""
    clear_folders() ; print('=== CLEAR DATA FOLDERS ===\n')
    fetch()         ; print('=== FETCH TICKERS ===\n')
    ind()           ; print('=== RUN INDICATORS ===\n')
    scan()          ; print('=== RUN SCANNER ===\n')

# UTILITIES -----------------------------------------------

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

def clear_folder(folder_path):
    """Clear a specific folder"""
    if folder_path.exists():
        for item in folder_path.glob('*'):
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Error deleting {item}: {e}")
        print(f"Cleared folder: {folder_path}")
    else:
        print(f"Folder does not exist: {folder_path}")

def clear_folders():
    """Clear all data folders"""
    folders = [TICKERS_DIR, INDICATORS_DIR, SCANNER_DIR]
    for folder in folders:
        clear_folder(folder)

def clear_screenshots():
    """Clear screenshots folder"""
    screenshots_dir = PROJECT_ROOT / "data" / "screenshots"
    clear_folder(screenshots_dir)

# COMMAND LINE INTERFACE (CLI) ----------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock Analysis Toolkit")

    parser.add_argument('--vis',      action='store_true', help='Launch visualization')
    parser.add_argument('--fetch',    action='store_true', help='Fetch ticker data')
    parser.add_argument('--ind',      action='store_true', help='Generate indicators')
    parser.add_argument('--scan',     action='store_true', help='Run scanner')
    parser.add_argument('--full-run', action='store_true', 
                        help='Complete pipeline: clear folders, fetch data, generate indicators, run scanner')

    parser.add_argument('--scan-file', type=str, default=None,
                        help='Specify scan file (e.g. "scan_results_300625.csv")')

    parser.add_argument('--clear-all',         action='store_true',
                        help='Clear all data folders (tickers, indicators, scanner)')
    parser.add_argument('--clear-tickers',     action='store_true',
                        help='Clear only the tickers data folder')
    parser.add_argument('--clear-indicators',  action='store_true',
                        help='Clear only the indicators data folder')
    parser.add_argument('--clear-scanner',     action='store_true',
                        help='Clear only the scanner results folder')
    parser.add_argument('--clear-screenshots', action='store_true',
                        help='Clear the screenshots folder')

    parser.add_argument('--list-scans', action='store_true',
                        help='Show available scan files')
    
    args = parser.parse_args()

    # Handle folder clearing first
    if   args.clear_all:         clear_folders()
    elif args.clear_tickers:     clear_folder(TICKERS_DIR)
    elif args.clear_indicators:  clear_folder(INDICATORS_DIR)
    elif args.clear_scanner:     clear_folder(SCANNER_DIR)
    elif args.clear_screenshots: clear_screenshots()

    # Then handle other commands
    elif args.list_scans:        list_scan_files()
    elif args.vis:               vis(scan_file=args.scan_file)
    elif args.fetch:             fetch()
    elif args.ind:               ind()
    elif args.scan:              scan()
    elif args.full_run:          full_run()
    else:
        print("""Available commands:
        Visualization:
          --vis                              Launch visualization
          --vis --scan-file "filename.csv"   Visualize specific scan
        
        Data Management:
          --fetch                            Fetch ticker data
          --ind                              Generate indicators
          --scan                             Run scanner
          --full-run                         Reset + Tickers + Indicators + Scanner
        
        Folder Management:
          --clear-all                        Clear all data folders
          --clear-tickers                    Clear only tickers data
          --clear-indicators                 Clear only indicators data
          --clear-scanner                    Clear only scanner results
          --clear-screenshots                Clear screenshots folder
        
        Utilities:
          --list-scans                       Show available scan files""")
