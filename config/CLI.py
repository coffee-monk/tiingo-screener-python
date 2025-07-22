import argparse
from pathlib import Path
from config.settings import (PROJECT_ROOT, 
                             SCANNER_DIR, 
                             INDICATORS_DIR, 
                             TICKERS_DIR, 
                             SCREENSHOTS_DIR)

# INITIALIZE CLI ------------------------------------------

def init_cli(
    vis,
    fetch,
    ind,
    scan
):
    """Single function that handles all CLI execution"""

    parser = argparse.ArgumentParser(description="Stock Analysis Toolkit")

    # Add all arguments
    parser.add_argument('--vis',               action='store_true', help='Launch visualization')
    parser.add_argument('--fetch',             action='store_true', help='Fetch ticker data')
    parser.add_argument('--ind',               action='store_true', help='Generate indicators')
    parser.add_argument('--scan',              action='store_true', help='Run scanner')
    parser.add_argument('--full-run',          action='store_true', help='Reset + Tickers + Indicators + Scanner')
    parser.add_argument('--clear-all',         action='store_true', help='Clear all data folders')
    parser.add_argument('--clear-tickers',     action='store_true', help='Clear only the tickers data folder')
    parser.add_argument('--clear-indicators',  action='store_true', help='Clear only the indicators data folder')
    parser.add_argument('--clear-scans',       action='store_true', help='Clear only the scans results folder') 
    parser.add_argument('--clear-screenshots', action='store_true', help='Clear the screenshots folder') 
    parser.add_argument('--list-scans',        action='store_true', help='Show available scan files')

    # argument inputs
    parser.add_argument('--ticker',    type=str, default=None, help='vis(ticker=ticker)')
    parser.add_argument('--scan-file', type=str, default=None, help='Specify scan file (e.g. "scan_results_300625.csv")')

    args = parser.parse_args()

    # Execute commands
    if   args.vis:               vis(ticker=args.ticker, scan_file=args.scan_file)
    elif args.fetch:             fetch()
    elif args.ind:               ind()
    elif args.scan:              scan()
    elif args.full_run:          full_run(fetch, ind, scan)
    elif args.clear_tickers:     clear_folder(TICKERS_DIR)
    elif args.clear_indicators:  clear_folder(INDICATORS_DIR)
    elif args.clear_scans:       clear_folder(SCANNER_DIR)
    elif args.clear_screenshots: clear_folder(SCREENSHOTS_DIR)
    elif args.clear_all:         clear_folders()
    elif args.list_scans:        list_scans()

    else: print("""\nAvailable commands:\n 
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
          --clear-scans                    Clear only scanner results
          --clear-screenshots                Clear screenshots folder
       
        Utilities:
          --list-scans                       Show available scan files\n"""
        )

# CLI UTILITY FUNCTIONS -----------------------------------

def list_scans():
    """List available scan files with dates"""
    print(f"\nScans folder: {SCANNER_DIR}")
    scans = sorted(SCANNER_DIR.glob("scan_results_*.csv"), 
                key=lambda f: f.stat().st_mtime, reverse=True)
    if not scans:
        print("\nNo scan files found in data/scans/\n")
        return
    
    print("\nAvailable scan files:")
    for i, scan in enumerate(scans[:10]):  # Show 10 most recent
        print(f"{i+1}. {scan.name}")
    print("\nUse with: --vis --scan-file 'filename.csv\n'")

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
        print(f"\nCleared folder: {folder_path}\n")
    else:
        print(f"\nFolder does not exist: {folder_path}")

def clear_folders():
    """Clear all data folders"""
    folders = [TICKERS_DIR, INDICATORS_DIR, SCANNER_DIR]
    for folder in folders:
        clear_folder(folder)

def full_run(fetch, ind, scan):
    """Clear folders + fetch data + generate indicators + run scanner"""
    clear_folders()
    fetch()         
    ind()           
    scan()          
