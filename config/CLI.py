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
    """Enhanced CLI with comprehensive version control"""
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
    parser.add_argument('--full-run-advanced', action='store_true', 
                       help='Full run with automated versioning')

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
    parser.add_argument('--delete-ind', type=str, metavar='NAME', help='Delete specific indicator version')
    parser.add_argument('--delete-ind-all', action='store_true', help='Delete ALL indicator versions')
    
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
    elif args.full_run_advanced: full_run_advanced(fetch, ind, scan)
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

# VERSION CONTROL ----------------------------------------

def save_indicator_version(version_name):
    """Save current indicators to a version folder"""
    version_dir = INDICATORS_DIR / version_name
    version_dir.mkdir(exist_ok=True)
    
    # Clear existing files in version folder
    for f in version_dir.glob('*'): f.unlink()
    
    # Copy current indicator files
    for f in INDICATORS_DIR.glob('*.csv'):
        shutil.copy2(f, version_dir)
    print(f"💾 Saved indicator version: {version_name}")

def load_indicator_version(version_name):
    """Load indicators from version to buffer"""
    version_dir = INDICATORS_DIR / version_name
    if not version_dir.exists():
        print(f"❌ Version '{version_name}' not found")
        return
    
    clear_indicator_buffer()
    for f in version_dir.glob('*'):
        shutil.copy2(f, INDICATORS_DIR)
    print(f"🔄 Loaded indicator version: {version_name}")

def save_scan_version(version_name):
    """Save current scans to a version folder"""
    version_dir = SCANNER_DIR / version_name
    version_dir.mkdir(exist_ok=True)
    
    for f in version_dir.glob('*'): f.unlink()
    for f in SCANNER_DIR.glob('scan_results_*.csv'):
        shutil.copy2(f, version_dir)
    print(f"💾 Saved scan version: {version_name}")

def load_scan_version(version_name):
    """Load scans from version to buffer"""
    version_dir = SCANNER_DIR / version_name
    if not version_dir.exists():
        print(f"❌ Scan version '{version_name}' not found")
        return
    
    clear_scan_buffer()
    for f in version_dir.glob('*'):
        shutil.copy2(f, SCANNER_DIR)
    print(f"🔄 Loaded scan version: {version_name}")

# LISTING FUNCTIONS --------------------------------------

def list_indicator_versions():
    """List all saved indicator versions"""
    versions = [d for d in INDICATORS_DIR.iterdir() if d.is_dir()]
    if not versions:
        print("\nNo indicator versions found")
        return
    
    print("\n📚 Indicator versions:")
    for i, version in enumerate(sorted(versions)):
        count = len(list(version.glob('*.csv')))
        print(f"  {i+1}. {version.name} ({count} files)")

def list_scan_versions():
    """List all saved scan versions"""
    versions = [d for d in SCANNER_DIR.iterdir() if d.is_dir()]
    if not versions:
        print("\nNo scan versions found")
        return
    
    print("\n📚 Scan versions:")
    for i, version in enumerate(sorted(versions)):
        count = len(list(version.glob('*.csv')))
        print(f"  {i+1}. {version.name} ({count} files)")

def list_scan_buffer_files():
    """List current scan files in buffer"""
    scans = sorted(SCANNER_DIR.glob("scan_results_*.csv"), 
                  key=lambda f: f.stat().st_mtime, reverse=True)
    
    print(f"\nCurrent scans in buffer ({len(scans)}):")
    for i, scan in enumerate(scans[:10]):
        print(f"  {i+1}. {scan.name}")

# DELETION FUNCTIONS -------------------------------------

def delete_indicator_version(version_name):
    """Delete specific indicator version"""
    version_dir = INDICATORS_DIR / version_name
    if not version_dir.exists():
        print(f"❌ Version '{version_name}' not found")
        return
    
    shutil.rmtree(version_dir)
    print(f"🗑️ Deleted indicator version: {version_name}")

def delete_scan_version(version_name):
    """Delete specific scan version"""
    version_dir = SCANNER_DIR / version_name
    if not version_dir.exists():
        print(f"❌ Scan version '{version_name}' not found")
        return
    
    shutil.rmtree(version_dir)
    print(f"🗑️ Deleted scan version: {version_name}")

def delete_all_indicator_versions():
    """Delete ALL indicator versions with confirmation"""
    versions = [d for d in INDICATORS_DIR.iterdir() if d.is_dir()]
    if not versions:
        print("\nNo indicator versions to delete")
        return
    
    print("\n⚠️ This will delete ALL indicator versions:")
    for v in sorted(versions): print(f"  - {v.name}")
    
    if input("\nType 'DELETE' to confirm: ").strip().upper() == "DELETE":
        for v in versions: shutil.rmtree(v)
        print(f"🔥 Deleted {len(versions)} indicator versions")
    else:
        print("Operation cancelled")

def delete_all_scan_versions():
    """Delete ALL scan versions with confirmation"""
    versions = [d for d in SCANNER_DIR.iterdir() if d.is_dir()]
    if not versions:
        print("\nNo scan versions to delete")
        return
    
    print("\n⚠️ This will delete ALL scan versions:")
    for v in sorted(versions): print(f"  - {v.name}")
    
    if input("\nType 'DELETE' to confirm: ").strip().upper() == "DELETE":
        for v in versions: shutil.rmtree(v)
        print(f"🔥 Deleted {len(versions)} scan versions")
    else:
        print("Operation cancelled")

# BUFFER MANAGEMENT --------------------------------------

def clear_indicator_buffer():
    """Clear only indicator files (preserves versions)"""
    count = sum(1 for f in INDICATORS_DIR.glob('*.csv') if f.unlink())
    print(f"\n🧹 Cleared {count} indicator files from buffer")

def clear_scan_buffer():
    """Clear only scan files (preserves versions)"""
    count = sum(1 for f in SCANNER_DIR.glob('scan_results_*.csv') if f.unlink())
    print(f"\n🧹 Cleared {count} scan files from buffer")

def clear_folder(folder_path):
    """Completely clear a folder"""
    if not folder_path.exists(): return
    
    count = 0
    for item in folder_path.glob('*'):
        try:
            if item.is_file():
                item.unlink()
                count += 1
            elif item.is_dir():
                shutil.rmtree(item)
                count += 1
        except Exception as e:
            print(f"Error deleting {item}: {e}")
    print(f"\n🧹 Cleared {count} items from {folder_path.name}")

def clear_all_folders_safe():
    """Clear all data while preserving versions"""
    clear_folder(TICKERS_DIR)
    clear_indicator_buffer()
    clear_scan_buffer()
    clear_folder(SCREENSHOTS_DIR)
    print("\n✨ All buffers cleared (versions preserved)")

# WORKFLOWS ----------------------------------------------

def full_run(fetch, ind, scan):
    """Basic full run pipeline"""
    clear_all_folders_safe()
    fetch()
    ind()
    scan()
    print("\n✅ Standard full run completed")

def full_run_advanced(fetch, ind, scan):
    """Enhanced full run with automated versioning"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # 1. Clear and fetch
    clear_all_folders_safe()
    fetch()
    
    # 2. Generate and save indicator versions
    ind()
    save_indicator_version(f"indicators_{timestamp}")
    
    # 3. Run and save scan versions
    scan()
    save_scan_version(f"scans_{timestamp}")
    
    print(f"\n🚀 Advanced full run completed at {timestamp}")
    print(f"  - Saved indicators: indicators_{timestamp}")
    print(f"  - Saved scans: scans_{timestamp}")

# HELP ---------------------------------------------------

def show_help():
    """Display comprehensive help"""
    print("""
Stock Analysis Toolkit - Command Reference:

CORE WORKFLOWS:
  --full-run           Standard pipeline (fetch + indicators + scan)
  --full-run-advanced  Enhanced pipeline with auto-versioning

DATA PROCESSING:
  --fetch              Download ticker data
  --ind                Calculate indicators
  --scan               Run scanner

VERSION CONTROL:
INDICATORS:
  --save-ind NAME      Save current indicators
  --load-ind NAME      Load indicator version  
  --list-ind           List indicator versions
  --delete-ind NAME    Delete specific version
  --delete-ind-all     Delete ALL indicator versions

SCANS:
  --save-scan NAME     Save current scans
  --load-scan NAME     Load scan version
  --list-scans-ver     List scan versions
  --delete-scan NAME   Delete specific version  
  --delete-scan-all    Delete ALL scan versions

FOLDER MANAGEMENT:
  --clear-all          Reset all folders (keep versions)
  --clear-tickers      Clear ticker data
  --clear-indicators   Clear indicator buffer
  --clear-scans        Clear scan buffer
  --clear-screenshots  Clear screenshots

UTILITIES:
  --list-scans         Show current scan files
  --vis                Launch visualization
""")
