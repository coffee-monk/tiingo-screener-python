from pathlib import Path
from datetime import datetime

# GLOBAL Variables

DATE_STAMP = datetime.now().strftime('%d%m%y')
 
# Project ROOT Directory

PROJECT_ROOT = Path(__file__).parent.parent

# Data Output Directories

SCANNER_DIR     = PROJECT_ROOT / "data" / "scans"
INDICATORS_DIR  = PROJECT_ROOT / "data" / "indicators"
TICKERS_DIR     = PROJECT_ROOT / "data" / "tickers"
SCREENSHOTS_DIR = PROJECT_ROOT / "data" / "screenshots"

# List Directories

# TSX, QQQ, NASDAQ
TICKERS_LIST    = PROJECT_ROOT / 'src/fetch_data/ticker_lists/TSX.csv'
