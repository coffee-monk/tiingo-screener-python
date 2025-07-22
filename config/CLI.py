# import argparse
# from pathlib import Path
# from config.settings import (PROJECT_ROOT, 
#                              SCANNER_DIR, 
#                              INDICATORS_DIR, 
#                              TICKERS_DIR, 
#                              SCREENSHOTS_DIR)
#
# # INITIALIZE CLI ------------------------------------------
#
# def init_cli(
#     vis,
#     fetch,
#     ind,
#     scan
# ):
#     """Single function that handles all CLI execution"""
#
#     parser = argparse.ArgumentParser(description="Stock Analysis Toolkit")
#
#     # Add all arguments
#     parser.add_argument('--vis',               action='store_true', help='Launch visualization')
#     parser.add_argument('--fetch',             action='store_true', help='Fetch ticker data')
#     parser.add_argument('--ind',               action='store_true', help='Generate indicators')
#     parser.add_argument('--scan',              action='store_true', help='Run scanner')
#     parser.add_argument('--full-run',          action='store_true', help='Reset + Tickers + Indicators + Scanner')
#     parser.add_argument('--clear-all',         action='store_true', help='Clear all data folders')
#     parser.add_argument('--clear-tickers',     action='store_true', help='Clear only the tickers data folder')
#     parser.add_argument('--clear-indicators',  action='store_true', help='Clear only the indicators data folder')
#     parser.add_argument('--clear-scans',       action='store_true', help='Clear only the scans results folder') 
#     parser.add_argument('--clear-screenshots', action='store_true', help='Clear the screenshots folder') 
#     parser.add_argument('--list-scans',        action='store_true', help='Show available scan files')
#
#     # argument inputs
#     parser.add_argument('--ticker',    type=str, default=None, help='vis(ticker=ticker)')
#     parser.add_argument('--scan-file', type=str, default=None, help='Specify scan file (e.g. "scan_results_300625.csv")')
#
#     args = parser.parse_args()
#
#     # Execute commands
#     if   args.vis:               vis(ticker=args.ticker, scan_file=args.scan_file)
#     elif args.fetch:             fetch()
#     elif args.ind:               ind()
#     elif args.scan:              scan()
#     elif args.full_run:          full_run(fetch, ind, scan)
#     elif args.clear_tickers:     clear_folder(TICKERS_DIR)
#     elif args.clear_indicators:  clear_folder(INDICATORS_DIR)
#     elif args.clear_scans:       clear_folder(SCANNER_DIR)
#     elif args.clear_screenshots: clear_folder(SCREENSHOTS_DIR)
#     elif args.clear_all:         clear_folders()
#     elif args.list_scans:        list_scans()
#
#     else: print("""\nAvailable commands:\n 
#         Visualization:
#           --vis                              Launch visualization
#           --vis --scan-file "filename.csv"   Visualize specific scan
#       
#         Data Management:
#           --fetch                            Fetch ticker data
#           --ind                              Generate indicators
#           --scan                             Run scanner
#           --full-run                         Reset + Tickers + Indicators + Scanner
#       
#         Folder Management:
#           --clear-all                        Clear all data folders
#           --clear-tickers                    Clear only tickers data
#           --clear-indicators                 Clear only indicators data
#           --clear-scans                    Clear only scanner results
#           --clear-screenshots                Clear screenshots folder
#       
#         Utilities:
#           --list-scans                       Show available scan files\n"""
#         )
#
# # CLI UTILITY FUNCTIONS -----------------------------------
#
# def list_scans():
#     """List available scan files with dates"""
#     print(f"\nScans folder: {SCANNER_DIR}")
#     scans = sorted(SCANNER_DIR.glob("scan_results_*.csv"), 
#                 key=lambda f: f.stat().st_mtime, reverse=True)
#     if not scans:
#         print("\nNo scan files found in data/scans/\n")
#         return
#    
#     print("\nAvailable scan files:")
#     for i, scan in enumerate(scans[:10]):  # Show 10 most recent
#         print(f"{i+1}. {scan.name}")
#     print("\nUse with: --vis --scan-file 'filename.csv\n'")
#
# def clear_folder(folder_path):
#     """Clear a specific folder"""
#     if folder_path.exists():
#         for item in folder_path.glob('*'):
#             try:
#                 if item.is_file():
#                     item.unlink()
#                 elif item.is_dir():
#                     shutil.rmtree(item)
#             except Exception as e:
#                 print(f"Error deleting {item}: {e}")
#         print(f"\nCleared folder: {folder_path}\n")
#     else:
#         print(f"\nFolder does not exist: {folder_path}")
#
# def clear_folders():
#     """Clear all data folders"""
#     folders = [TICKERS_DIR, INDICATORS_DIR, SCANNER_DIR]
#     for folder in folders:
#         clear_folder(folder)
#
# def full_run(fetch, ind, scan):
#     """Clear folders + fetch data + generate indicators + run scanner"""
#     clear_folders()
#     fetch()         
#     ind()           
#     scan()          




import argparse
import shutil
from pathlib import Path
from config.settings import (PROJECT_ROOT, 
                           SCANNER_DIR, 
                           INDICATORS_DIR, 
                           TICKERS_DIR, 
                           SCREENSHOTS_DIR)

# INITIALIZE CLI ------------------------------------------

def init_cli(vis, fetch, ind, scan):
    """Enhanced CLI with version control for both indicators and scans"""
    parser = argparse.ArgumentParser(description="Stock Analysis Toolkit")

    # Visualization
    parser.add_argument('--vis', action='store_true', help='Launch visualization')
    parser.add_argument('--ticker', type=str, default=None, help='Specify ticker for visualization')
    parser.add_argument('--scan-file', type=str, default=None, help='Specify scan file')

    # Data processing
    parser.add_argument('--fetch', action='store_true', help='Fetch ticker data')
    parser.add_argument('--ind', action='store_true', help='Generate indicators')
    parser.add_argument('--scan', action='store_true', help='Run scanner')
    parser.add_argument('--full-run', action='store_true', help='Reset + Tickers + Indicators + Scanner')

    # Folder management
    parser.add_argument('--clear-all', action='store_true', help='Clear all data folders (preserves versions)')
    parser.add_argument('--clear-tickers', action='store_true', help='Clear tickers data')
    parser.add_argument('--clear-indicators', action='store_true', help='Clear only indicator buffer files')
    parser.add_argument('--clear-scans', action='store_true', help='Clear only scan buffer files')
    parser.add_argument('--clear-screenshots', action='store_true', help='Clear screenshots')

    # Indicator version control
    parser.add_argument('--save-ind', type=str, metavar='NAME', help='Save current indicators as version')
    parser.add_argument('--load-ind', type=str, metavar='NAME', help='Load specific indicator version')
    parser.add_argument('--list-ind', action='store_true', help='List available indicator versions')
    parser.add_argument('--delete-ind', type=str, metavar='NAME', help='Delete specific indicator version')
    parser.add_argument('--delete-ind-all', action='store_true', help='Delete ALL indicator versions')

    # Scan version control
    parser.add_argument('--save-scan', type=str, metavar='NAME', help='Save current scans as version')
    parser.add_argument('--load-scan', type=str, metavar='NAME', help='Load specific scan version')
    parser.add_argument('--list-scans-ver', action='store_true', help='List available scan versions')
    parser.add_argument('--delete-scan', type=str, metavar='NAME', help='Delete specific scan version')
    parser.add_argument('--delete-scan-all', action='store_true', help='Delete ALL scan versions')

    # Utilities
    parser.add_argument('--list-scans', action='store_true', help='Show available scan files in buffer')

    args = parser.parse_args()

    # Execute commands
    if args.vis: vis(ticker=args.ticker, scan_file=args.scan_file)
    elif args.fetch: fetch()
    elif args.ind: ind()
    elif args.scan: scan()
    elif args.full_run: full_run(fetch, ind, scan)
    elif args.clear_tickers: clear_folder(TICKERS_DIR)
    elif args.clear_indicators: clear_indicator_buffer()
    elif args.clear_scans: clear_scan_buffer()
    elif args.clear_screenshots: clear_folder(SCREENSHOTS_DIR)
    elif args.clear_all: clear_all_folders_safe()
    elif args.list_scans: list_scan_buffer_files()
    elif args.list_ind: list_indicator_versions()
    elif args.list_scans_ver: list_scan_versions()
    elif args.save_ind: save_indicator_version(args.save_ind)
    elif args.load_ind: load_indicator_version(args.load_ind)
    elif args.delete_ind: delete_indicator_version(args.delete_ind)
    elif args.delete_ind_all: delete_all_indicator_versions()
    elif args.save_scan: save_scan_version(args.save_scan)
    elif args.load_scan: load_scan_version(args.load_scan)
    elif args.delete_scan: delete_scan_version(args.delete_scan)
    elif args.delete_scan_all: delete_all_scan_versions()
    else: show_help()

# SCAN VERSION CONTROL -----------------------------------

def save_scan_version(version_name):
    """Save current scan files as a named version"""
    version_dir = SCANNER_DIR / version_name
    version_dir.mkdir(exist_ok=True)
    
    # Clear existing version files
    for f in version_dir.glob('*'):
        f.unlink()
    
    # Copy only scan files from buffer
    for f in SCANNER_DIR.glob('scan_results_*.csv'):
        if f.is_file():
            shutil.copy2(f, version_dir)
    print(f"💾 Saved current scans as version: '{version_name}'")

def load_scan_version(version_name):
    """Load a scan version into the buffer zone"""
    version_dir = SCANNER_DIR / version_name
    
    if not version_dir.exists():
        print(f"❌ Scan version '{version_name}' not found")
        return
    
    # Clear scan buffer
    clear_scan_buffer()
    
    # Copy version files to buffer
    for f in version_dir.glob('*'):
        if f.is_file():
            shutil.copy2(f, SCANNER_DIR)
    print(f"🔄 Loaded scan version: '{version_name}'")

def list_scan_versions():
    """List available scan versions"""
    versions = [d for d in SCANNER_DIR.iterdir() if d.is_dir()]
    if not versions:
        print("\nNo scan versions found")
        return
    
    print("\n📚 Available scan versions:")
    for i, version in enumerate(sorted(versions)):
        file_count = len(list(version.glob('*.csv')))
        print(f"  {i+1}. {version.name} ({file_count} files)")

def delete_scan_version(version_name):
    """Delete a specific scan version"""
    version_dir = SCANNER_DIR / version_name
    
    if not version_dir.exists():
        print(f"❌ Scan version '{version_name}' not found")
        return
    
    shutil.rmtree(version_dir)
    print(f"🗑️ Deleted scan version: '{version_name}'")

def delete_all_scan_versions():
    """Delete ALL scan versions with confirmation"""
    versions = [d for d in SCANNER_DIR.iterdir() if d.is_dir()]
    if not versions:
        print("\nNo scan versions found to delete")
        return
    
    print("\n⚠️ This will PERMANENTLY delete ALL scan versions:")
    for version in sorted(versions):
        file_count = len(list(version.glob('*.csv')))
        print(f"  - {version.name} ({file_count} files)")
    
    confirm = input("\nType 'DELETE' to confirm or anything else to cancel: ")
    if confirm.strip().upper() == "DELETE":
        for version in versions:
            shutil.rmtree(version)
        print(f"🔥 Deleted {len(versions)} scan versions")
    else:
        print("Operation cancelled - scan versions remain unchanged")

def clear_scan_buffer():
    """Clear only the scan buffer files (preserves version folders)"""
    deleted_files = 0
    for f in SCANNER_DIR.glob('scan_results_*.csv'):
        if f.is_file():
            f.unlink()
            deleted_files += 1
    print(f"\n🧹 Cleared {deleted_files} files from scan buffer (preserved versions)")

# INDICATOR VERSION CONTROL ------------------------------

def save_indicator_version(version_name):
    """Save current indicator files as a named version"""
    version_dir = INDICATORS_DIR / version_name
    version_dir.mkdir(exist_ok=True)
    
    # Clear existing version files
    for f in version_dir.glob('*'):
        f.unlink()
    
    # Copy only CSV files from buffer
    for f in INDICATORS_DIR.glob('*.csv'):
        if f.is_file():
            shutil.copy2(f, version_dir)
    print(f"💾 Saved current indicators as version: '{version_name}'")

def load_indicator_version(version_name):
    """Load a version into the buffer zone"""
    version_dir = INDICATORS_DIR / version_name
    
    if not version_dir.exists():
        print(f"❌ Version '{version_name}' not found")
        return
    
    # Clear buffer zone (only CSV files)
    clear_indicator_buffer()
    
    # Copy version files to buffer
    for f in version_dir.glob('*'):
        if f.is_file():
            shutil.copy2(f, INDICATORS_DIR)
    print(f"🔄 Loaded version: '{version_name}'")

def list_indicator_versions():
    """List available indicator versions"""
    versions = [d for d in INDICATORS_DIR.iterdir() if d.is_dir()]
    if not versions:
        print("\nNo indicator versions found")
        return
    
    print("\n📚 Available indicator versions:")
    for i, version in enumerate(sorted(versions)):
        file_count = len(list(version.glob('*.csv')))
        print(f"  {i+1}. {version.name} ({file_count} files)")

def delete_indicator_version(version_name):
    """Delete a specific indicator version"""
    version_dir = INDICATORS_DIR / version_name
    
    if not version_dir.exists():
        print(f"❌ Version '{version_name}' not found")
        return
    
    shutil.rmtree(version_dir)
    print(f"🗑️ Deleted version: '{version_name}'")

def delete_all_indicator_versions():
    """Delete ALL indicator versions with confirmation"""
    versions = [d for d in INDICATORS_DIR.iterdir() if d.is_dir()]
    if not versions:
        print("\nNo indicator versions found to delete")
        return
    
    print("\n⚠️ This will PERMANENTLY delete ALL indicator versions:")
    for version in sorted(versions):
        file_count = len(list(version.glob('*.csv')))
        print(f"  - {version.name} ({file_count} files)")
    
    confirm = input("\nType 'DELETE' to confirm or anything else to cancel: ")
    if confirm.strip().upper() == "DELETE":
        for version in versions:
            shutil.rmtree(version)
        print(f"🔥 Deleted {len(versions)} indicator versions")
    else:
        print("Operation cancelled - versions remain unchanged")

def clear_indicator_buffer():
    """Clear only the indicator buffer files (preserves version folders)"""
    deleted_files = 0
    for f in INDICATORS_DIR.glob('*.csv'):
        if f.is_file():
            f.unlink()
            deleted_files += 1
    print(f"\n🧹 Cleared {deleted_files} files from indicator buffer (preserved versions)")

# FOLDER MANAGEMENT --------------------------------------

def clear_all_folders_safe():
    """Clear all data folders while preserving versions"""
    clear_folder(TICKERS_DIR)
    clear_indicator_buffer()
    clear_scan_buffer()
    print("\n🧹 Cleared all data folders (preserved versions)")

def clear_folder(folder_path):
    """Clear a specific folder completely"""
    if folder_path.exists():
        for item in folder_path.glob('*'):
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Error deleting {item}: {e}")
        print(f"\n🧹 Cleared folder: {folder_path}")
    else:
        print(f"\nFolder does not exist: {folder_path}")

# UTILITIES ----------------------------------------------

def list_scan_buffer_files():
    """List available scan files in buffer"""
    print(f"\nScan buffer folder: {SCANNER_DIR}")
    scans = sorted(SCANNER_DIR.glob("scan_results_*.csv"), 
                 key=lambda f: f.stat().st_mtime, reverse=True)
    if not scans:
        print("\nNo scan files found in buffer\n")
        return
    
    print("\nAvailable scan files in buffer:")
    for i, scan in enumerate(scans[:10]):
        print(f"{i+1}. {scan.name}")
    print("\nUse with: --vis --scan-file 'filename.csv'")

def show_help():
    """Show enhanced help with version control"""
    print("""
Stock Analysis Toolkit - Available Commands:

Data Processing:
  --fetch              Fetch ticker data
  --ind                Generate indicators
  --scan               Run scanner
  --full-run           Reset + Tickers + Indicators + Scanner

Visualization:
  --vis                Launch visualization
  --vis --ticker AAPL  Visualize specific ticker
  --vis --scan-file X  Visualize specific scan file

Indicator Versions:
  --save-ind NAME      Save current indicators as version
  --load-ind NAME      Load specific indicator version
  --list-ind           List available indicator versions
  --delete-ind NAME    Delete specific indicator version
  --delete-ind-all     Delete ALL indicator versions

Scan Versions:
  --save-scan NAME     Save current scans as version
  --load-scan NAME     Load specific scan version
  --list-scans-ver     List available scan versions
  --delete-scan NAME   Delete specific scan version
  --delete-scan-all    Delete ALL scan versions

Folder Management:
  --clear-all          Clear all data folders (preserves versions)
  --clear-tickers      Clear tickers data
  --clear-indicators   Clear only indicator buffer files
  --clear-scans        Clear only scan buffer files
  --clear-screenshots  Clear screenshots

Utilities:
  --list-scans         Show available scan files in buffer
""")

def full_run(fetch, ind, scan):
    """Clear folders + fetch data + generate indicators + run scanner"""
    clear_all_folders_safe()
    fetch()         
    ind()           
    scan()
