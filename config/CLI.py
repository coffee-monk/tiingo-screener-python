from pathlib import Path
import argparse
from config.data_manager import dm

def init_cli(vis, fetch, ind, scan, full_run):
    """Enhanced CLI using DataManager"""
    parser = argparse.ArgumentParser(description="Stock Analysis Toolkit")

    # Visualization
    parser.add_argument('--vis', action='store_true', help='Launch visualization')
    parser.add_argument('--ticker', type=str, default=None, help='Specify ticker for visualization')
    parser.add_argument('--scan-file', type=str, default=None, help='Specify scan file')
    parser.add_argument('--timeframe', type=str, default=None, help="Specify timeframe (eg '1hour')")
    parser.add_argument('--ver', type=str, default=None, help='Specify ind version (eg 1, 2, 3, 4)')

    # Data processing
    parser.add_argument('--fetch', action='store_true', help='Fetch ticker data')
    parser.add_argument('--ind', action='store_true', help='Generate indicators')
    parser.add_argument('--ind-conf', type=str, help='Indicator configuration to use')
    parser.add_argument('--scan', action='store_true', help='Run scanner')
    parser.add_argument('--scan-list', type=str, default=None, help='Specify scan list version')
    parser.add_argument('--full-run', action='store_true', help='Reset + Tickers + Indicators + Scanner')

    # Folder management
    parser.add_argument('--clear-all', action='store_true', help='Clear all data folders (preserves versions)')
    parser.add_argument('--clear-tickers', action='store_true', help='Clear tickers data')
    parser.add_argument('--clear-indicators', action='store_true', help='Clear only indicator buffer files')
    parser.add_argument('--clear-scans', action='store_true', help='Clear only scan buffer files')
    parser.add_argument('--clear-screenshots', action='store_true', help='Clear screenshots')

    # Version control - Indicators
    parser.add_argument('--save-ind', type=str, metavar='NAME', help='Save current indicators as version')
    parser.add_argument('--load-ind', type=str, metavar='NAME', help='Load specific indicator version')
    parser.add_argument('--list-ind', action='store_true', help='List available indicator files in buffer')
    parser.add_argument('--list-ind-ver', action='store_true', help='List available indicator versions')
    parser.add_argument('--delete-ind', type=str, metavar='NAME', help='Delete specific indicator version')
    parser.add_argument('--delete-ind-all', action='store_true', help='Delete ALL indicator versions')

    # Version control - Scans
    parser.add_argument('--save-scan', type=str, metavar='NAME', help='Save current scans as version')
    parser.add_argument('--load-scan', type=str, metavar='NAME', help='Load specific scan version')
    parser.add_argument('--list-scans', action='store_true', help='Show available scan files in buffer')
    parser.add_argument('--list-scans-ver', action='store_true', help='List available scan versions')
    parser.add_argument('--delete-scan', type=str, metavar='NAME', help='Delete specific scan version')
    parser.add_argument('--delete-scan-all', action='store_true', help='Delete ALL scan versions')

    # Version control - Tickers (new)
    parser.add_argument('--save-tickers', type=str, metavar='NAME', help='Save current tickers as version')
    parser.add_argument('--load-tickers', type=str, metavar='NAME', help='Load specific ticker version')
    parser.add_argument('--list-tickers', action='store_true', help='List available ticker files in buffer')
    parser.add_argument('--list-tickers-ver', action='store_true', help='List available ticker versions')
    parser.add_argument('--delete-tickers', type=str, metavar='NAME', help='Delete specific ticker version')
    parser.add_argument('--delete-tickers-all', action='store_true', help='Delete ALL ticker versions')
    parser.add_argument('--ticker-timeframe', type=str, default=None, 
                       help='Filter tickers by timeframe (e.g., daily, weekly)')

    args = parser.parse_args()

    # Execute commands
    if args.vis: vis(ticker=args.ticker, scan_file=args.scan_file, timeframe=args.timeframe, version=args.ver)
    elif args.fetch: fetch()
    elif args.ind: ind(args.ind_conf)
    elif args.scan: scan(args.scan_list)  # Modified to pass scan_list parameter
    elif args.full_run: full_run(fetch, ind, scan)
    elif args.clear_tickers: dm.clear_buffer(dm.tickers_dir)
    elif args.clear_indicators: dm.clear_buffer(dm.indicators_dir)
    elif args.clear_scans: dm.clear_buffer(dm.scanner_dir, "scan_results_*.csv")
    elif args.clear_screenshots: dm.clear_buffer(dm.screenshots_dir)
    elif args.clear_all: dm.clear_all_buffers()

    # Indicator commands
    elif args.list_ind: dm.list_ind()
    elif args.list_ind_ver: dm.list_versions(dm.indicators_dir, "Indicators")
    elif args.save_ind: dm.save_indicators(args.save_ind)
    elif args.load_ind: dm.load_version(dm.indicators_dir, args.load_ind)
    elif args.delete_ind: dm.delete_version(dm.indicators_dir, args.delete_ind)
    elif args.delete_ind_all: dm.delete_all_versions(dm.indicators_dir)

    # Scan commands
    elif args.list_scans: dm.list_scans()
    elif args.list_scans_ver: dm.list_versions(dm.scanner_dir, "Scan")
    elif args.save_scan: dm.save_scans(args.save_scan)
    elif args.load_scan: dm.load_version(dm.scanner_dir, args.load_scan, "scan_results_*.csv")
    elif args.delete_scan: dm.delete_version(dm.scanner_dir, args.delete_scan)
    elif args.delete_scan_all: dm.delete_all_versions(dm.scanner_dir)

    # Ticker commands (new)
    elif args.list_tickers: dm.list_tickers(timeframe=args.ticker_timeframe)
    elif args.list_tickers_ver: dm.list_versions(dm.tickers_dir, "Tickers")
    elif args.save_tickers: dm.save_tickers(args.save_tickers)
    elif args.load_tickers: dm.load_version(dm.tickers_dir, args.load_tickers)
    elif args.delete_tickers: dm.delete_version(dm.tickers_dir, args.delete_tickers)
    elif args.delete_tickers_all: dm.delete_all_versions(dm.tickers_dir)

    else: show_help()

def show_help() -> None:
    """Display comprehensive help"""
    print("""
  STOCK ANALYSIS TOOLKIT - COMMAND REFERENCE:

  CORE FUNCTIONS:
  --fetch                     Download ticker data
  --ind                       Calculate indicators
  --ind-conf CONFIG           Indicator configuration to use
  --scan                      Run scanner
  --scan-list VERSION         Specify scan list version (e.g., scan_list_1)
  --vis                       Launch visualization
  --ticker TICKER             Specify ticker for visualization (e.g., MSFT)
  --timeframe TIMEFRAME       Specify timeframe for visualization (e.g., d, w, 4h, h, 5min)
  --ver VERSION               Specify indicator version for visualization (e.g., 1, 2, 3, 4)
  --scan-file FILE            Specify scan file for visualization
  --full-run                  Standard pipeline (fetch + indicators + scan)

  DATA INSPECTION:
  --list-scans                Show recent scan files
  --list-ind                  Show recent indicator files
  --list-tickers              List available ticker files
  --ticker-timeframe          Filter tickers by timeframe (e.g., daily, weekly)
  --list-scans-ver            List saved scan versions
  --list-ind-ver              List saved indicator versions
  --list-tickers-ver          List saved ticker versions

  VERSION CONTROL:
  --save-ind NAME             Save current indicators
  --load-ind NAME             Load indicator version  
  --delete-ind NAME           Delete specific version
  --delete-ind-all            Delete ALL indicator versions
  --save-scan NAME            Save current scans
  --load-scan NAME            Load scan version
  --delete-scan NAME          Delete specific version  
  --delete-scan-all           Delete ALL scan versions
  --save-tickers NAME         Save current tickers
  --load-tickers NAME         Load ticker version
  --delete-tickers NAME       Delete specific ticker version
  --delete-tickers-all        Delete ALL ticker versions

  FOLDER MANAGEMENT:           
  --clear-all                 Reset all folders (keep versions)
  --clear-tickers             Clear ticker data
  --clear-indicators          Clear indicator buffer
  --clear-scans               Clear scan buffer
  --clear-screenshots         Clear screenshots
""")
