import argparse
from pathlib import Path

# Project ROOT and data folders
PROJECT_ROOT = Path(__file__).parent.parent
SCANNER_DIR     = PROJECT_ROOT / "data" / "scanner"
INDICATORS_DIR  = PROJECT_ROOT / "data" / "indicators"
TICKERS_DIR     = PROJECT_ROOT / "data" / "tickers"
SCREENSHOTS_DIR = PROJECT_ROOT / "data" / "screenshots"

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
    parser.add_argument('--clear-scanner',     action='store_true', help='Clear only the scanner results folder') 
    parser.add_argument('--clear-screenshots', action='store_true', help='Clear the screenshots folder') 
    parser.add_argument('--list-scans',        action='store_true', help='Show available scan files')
    parser.add_argument('--scan-file', type=str, default=None, help='Specify scan file (e.g. "scan_results_300625.csv")')
    parser.add_argument('--ticker', type=str, default=None, help='vis(ticker=ticker)')

    args = parser.parse_args()

    # Execute commands
    if   args.vis:               vis(scan_file=args.scan_file, ticker=args.ticker)
    elif args.fetch:             fetch()
    elif args.ind:               ind()
    elif args.scan:              scan()
    elif args.full_run:          full_run(fetch, ind, scan)
    elif args.clear_all:         clear_folders(TICKERS_DIR, INDICATORS_DIR, SCANNER_DIR)
    elif args.clear_tickers:     clear_folder(TICKERS_DIR)
    elif args.clear_indicators:  clear_folder(INDICATORS_DIR)
    elif args.clear_scanner:     clear_folder(SCANNER_DIR)
    elif args.clear_screenshots: clear_folder(SCREENSHOTS_DIR)
    elif args.list_scans:        list_scan_files(SCANNER_DIR)

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
          --clear-scanner                    Clear only scanner results
          --clear-screenshots                Clear screenshots folder
       
        Utilities:
          --list-scans                       Show available scan files\n"""
        )

# CLI UTILITY FUNCTIONS -----------------------------------

def list_scan_files(SCANNER_DIR):
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

def clear_folders(TICKERS_DIR, INDICATORS_DIR, SCANNER_DIR):
    """Clear all data folders"""
    folders = [TICKERS_DIR, INDICATORS_DIR, SCANNER_DIR]
    for folder in folders:
        clear_folder(folder)

def full_run(fetch, ind, scan):
    """Clear folders + fetch data + generate indicators + run scanner"""
    clear_folders(TICKERS_DIR, INDICATORS_DIR, SCANNER_DIR) ; print('=== CLEAR DATA FOLDERS ===\n')
    fetch() ; print('=== FETCH TICKERS ===\n')
    ind()   ; print('=== RUN INDICATORS ===\n')
    scan()  ; print('=== RUN SCANNER ===\n')
