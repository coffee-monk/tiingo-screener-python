# from pathlib import Path
# import argparse
# from config.data_manager import dm
#
# def init_cli(vis, fetch, ind, scan, full_run):
#     """Enhanced CLI using DataManager"""
#     parser = argparse.ArgumentParser(description="Stock Analysis Toolkit")
#
#     # Visualization
#     parser.add_argument('--vis', action='store_true', help='Launch visualization')
#     parser.add_argument('--ticker', type=str, default=None, help='Specify ticker for visualization')
#     parser.add_argument('--scan-file', type=str, default=None, help='Specify scan file')
#
#     # Data processing
#     parser.add_argument('--fetch', action='store_true', help='Fetch ticker data')
#     parser.add_argument('--ind', action='store_true', help='Generate indicators')
#     parser.add_argument('--scan', action='store_true', help='Run scanner')
#     parser.add_argument('--full-run', action='store_true', help='Reset + Tickers + Indicators + Scanner')
#
#     # Folder management
#     parser.add_argument('--clear-all', action='store_true', help='Clear all data folders (preserves versions)')
#     parser.add_argument('--clear-tickers', action='store_true', help='Clear tickers data')
#     parser.add_argument('--clear-indicators', action='store_true', help='Clear only indicator buffer files')
#     parser.add_argument('--clear-scans', action='store_true', help='Clear only scan buffer files')
#     parser.add_argument('--clear-screenshots', action='store_true', help='Clear screenshots')
#
#     # Version control
#     parser.add_argument('--save-ind', type=str, metavar='NAME', help='Save current indicators as version')
#     parser.add_argument('--load-ind', type=str, metavar='NAME', help='Load specific indicator version')
#     parser.add_argument('--list-ind', action='store_true', help='List available indicator versions')
#     parser.add_argument('--list-ind-ver', action='store_true', help='List available indicator versions')
#     parser.add_argument('--delete-ind', type=str, metavar='NAME', help='Delete specific indicator version')
#     parser.add_argument('--delete-ind-all', action='store_true', help='Delete ALL indicator versions')
#
#     parser.add_argument('--save-scan', type=str, metavar='NAME', help='Save current scans as version')
#     parser.add_argument('--load-scan', type=str, metavar='NAME', help='Load specific scan version')
#     parser.add_argument('--list-scans', action='store_true', help='Show available scan files in buffer')
#     parser.add_argument('--list-scans-ver', action='store_true', help='List available scan versions')
#     parser.add_argument('--delete-scan', type=str, metavar='NAME', help='Delete specific scan version')
#     parser.add_argument('--delete-scan-all', action='store_true', help='Delete ALL scan versions')
#
#     args = parser.parse_args()
#
#     # Execute commands
#     if args.vis: vis(ticker=args.ticker, scan_file=args.scan_file)
#     elif args.fetch: fetch()
#     elif args.ind: ind()
#     elif args.scan: scan()
#     elif args.full_run: full_run(fetch, ind, scan)
#     elif args.clear_tickers: dm.clear_buffer(dm.tickers_dir)
#     elif args.clear_indicators: dm.clear_buffer(dm.indicators_dir)
#     elif args.clear_scans: dm.clear_buffer(dm.scanner_dir, "scan_results_*.csv")
#     elif args.clear_screenshots: dm.clear_buffer(dm.screenshots_dir)
#     elif args.clear_all: dm.clear_all_buffers()
#     elif args.list_scans: dm.list_scans()
#     elif args.list_ind: dm.list_ind()
#     elif args.list_scans_ver: dm.list_versions(dm.scanner_dir, "Scan")
#     elif args.list_ind_ver: dm.list_versions(dm.indicators_dir, "Indicators")
#     elif args.save_ind: dm.save_indicators(args.save_ind)
#     elif args.load_ind: dm.load_version(dm.indicators_dir, args.load_ind)
#     elif args.delete_ind: dm.delete_version(dm.indicators_dir, args.delete_ind)
#     elif args.delete_ind_all: dm.delete_all_versions(dm.indicators_dir)
#     elif args.save_scan: dm.save_scans(args.save_scan)
#     elif args.load_scan: dm.load_version(dm.scanner_dir, args.load_scan, "scan_results_*.csv")
#     elif args.delete_scan: dm.delete_version(dm.scanner_dir, args.delete_scan)
#     elif args.delete_scan_all: dm.delete_all_versions(dm.scanner_dir)
#     else: show_help()
#
# def show_help() -> None:
#     """Display comprehensive help"""
#     print("""
# STOCK ANALYSIS TOOLKIT - COMMAND REFERENCE:
#
# CORE FUNCTIONS:
#
#   --fetch              Download ticker data
#   --ind                Calculate indicators
#   --scan               Run scanner
#   --vis                Launch visualization
#   --full-run           Standard pipeline (fetch + indicators + scan)
#
# DATA INSPECTION:
#
#   --list-scans         Show recent scan files
#   --list-ind           Show recent indicator files
#   --list-scans-ver     List saved scan versions
#   --list-ind-ver       List saved indicator versions
#
# VERSION CONTROL:
#
#   --save-ind NAME      Save current indicators
#   --load-ind NAME      Load indicator version  
#   --delete-ind NAME    Delete specific version
#   --delete-ind-all     Delete ALL indicator versions
#
#   --save-scan NAME     Save current scans
#   --load-scan NAME     Load scan version
#   --delete-scan NAME   Delete specific version  
#   --delete-scan-all    Delete ALL scan versions
#
# FOLDER MANAGEMENT:
#
#   --clear-all          Reset all folders (keep versions)
#   --clear-tickers      Clear ticker data
#   --clear-indicators   Clear indicator buffer
#   --clear-scans        Clear scan buffer
#   --clear-screenshots  Clear screenshots
# """)




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

    # Data processing
    parser.add_argument('--fetch', action='store_true', help='Fetch ticker data')
    parser.add_argument('--ind', action='store_true', help='Generate indicators')
    parser.add_argument('--ind-conf', type=str, help='Indicator configuration to use')
    parser.add_argument('--scan', action='store_true', help='Run scanner')
    parser.add_argument('--full-run', action='store_true', help='Reset + Tickers + Indicators + Scanner')

    # Folder management
    parser.add_argument('--clear-all', action='store_true', help='Clear all data folders (preserves versions)')
    parser.add_argument('--clear-tickers', action='store_true', help='Clear tickers data')
    parser.add_argument('--clear-indicators', action='store_true', help='Clear only indicator buffer files')
    parser.add_argument('--clear-scans', action='store_true', help='Clear only scan buffer files')
    parser.add_argument('--clear-screenshots', action='store_true', help='Clear screenshots')

    # Version control
    parser.add_argument('--save-ind', type=str, metavar='NAME', help='Save current indicators as version')
    parser.add_argument('--load-ind', type=str, metavar='NAME', help='Load specific indicator version')
    parser.add_argument('--list-ind', action='store_true', help='List available indicator versions')
    parser.add_argument('--list-ind-ver', action='store_true', help='List available indicator versions')
    parser.add_argument('--delete-ind', type=str, metavar='NAME', help='Delete specific indicator version')
    parser.add_argument('--delete-ind-all', action='store_true', help='Delete ALL indicator versions')

    parser.add_argument('--save-scan', type=str, metavar='NAME', help='Save current scans as version')
    parser.add_argument('--load-scan', type=str, metavar='NAME', help='Load specific scan version')
    parser.add_argument('--list-scans', action='store_true', help='Show available scan files in buffer')
    parser.add_argument('--list-scans-ver', action='store_true', help='List available scan versions')
    parser.add_argument('--delete-scan', type=str, metavar='NAME', help='Delete specific scan version')
    parser.add_argument('--delete-scan-all', action='store_true', help='Delete ALL scan versions')

    args = parser.parse_args()

    # Execute commands
    if args.vis: vis(ticker=args.ticker, scan_file=args.scan_file)
    elif args.fetch: fetch()
    elif args.ind: ind(args.ind_conf)
    elif args.scan: scan()
    elif args.full_run: full_run(fetch, ind, scan)
    elif args.clear_tickers: dm.clear_buffer(dm.tickers_dir)
    elif args.clear_indicators: dm.clear_buffer(dm.indicators_dir)
    elif args.clear_scans: dm.clear_buffer(dm.scanner_dir, "scan_results_*.csv")
    elif args.clear_screenshots: dm.clear_buffer(dm.screenshots_dir)
    elif args.clear_all: dm.clear_all_buffers()
    elif args.list_scans: dm.list_scans()
    elif args.list_ind: dm.list_ind()
    elif args.list_scans_ver: dm.list_versions(dm.scanner_dir, "Scan")
    elif args.list_ind_ver: dm.list_versions(dm.indicators_dir, "Indicators")
    elif args.save_ind: dm.save_indicators(args.save_ind)
    elif args.load_ind: dm.load_version(dm.indicators_dir, args.load_ind)
    elif args.delete_ind: dm.delete_version(dm.indicators_dir, args.delete_ind)
    elif args.delete_ind_all: dm.delete_all_versions(dm.indicators_dir)
    elif args.save_scan: dm.save_scans(args.save_scan)
    elif args.load_scan: dm.load_version(dm.scanner_dir, args.load_scan, "scan_results_*.csv")
    elif args.delete_scan: dm.delete_version(dm.scanner_dir, args.delete_scan)
    elif args.delete_scan_all: dm.delete_all_versions(dm.scanner_dir)
    else: show_help()

def show_help() -> None:
    """Display comprehensive help"""
    print("""
STOCK ANALYSIS TOOLKIT - COMMAND REFERENCE:

CORE FUNCTIONS:
  --fetch              Download ticker data
  --ind                Calculate indicators
  --ind-conf CONFIG    Indicator configuration to use
  --scan               Run scanner
  --vis                Launch visualization
  --full-run           Standard pipeline (fetch + indicators + scan)

DATA INSPECTION:
  --list-scans         Show recent scan files
  --list-ind           Show recent indicator files
  --list-scans-ver     List saved scan versions
  --list-ind-ver       List saved indicator versions

VERSION CONTROL:
  --save-ind NAME      Save current indicators
  --load-ind NAME      Load indicator version  
  --delete-ind NAME    Delete specific version
  --delete-ind-all     Delete ALL indicator versions

  --save-scan NAME     Save current scans
  --load-scan NAME     Load scan version
  --delete-scan NAME   Delete specific version  
  --delete-scan-all    Delete ALL scan versions

FOLDER MANAGEMENT:
  --clear-all          Reset all folders (keep versions)
  --clear-tickers      Clear ticker data
  --clear-indicators   Clear indicator buffer
  --clear-scans        Clear scan buffer
  --clear-screenshots  Clear screenshots
""")
