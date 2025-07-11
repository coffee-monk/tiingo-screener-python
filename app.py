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
from src.scanner.scan_configs.scan_configs import scan_configs
from src.indicators.ind_configs.ind_configs import indicators, params
from src.CLI import init_cli, SCANNER_DIR, list_scan_files

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

# VISUALIZATION ------------------------------------------

def vis(scan_file=None):

    if not scan_file:

        ticker = 'SOFI'

        # df1 = fetch_ticker(timeframe='d', ticker=ticker, api_key=API_KEY)
        df2 = fetch_ticker(timeframe='d', ticker=ticker, api_key=API_KEY)
        # df3 = fetch_ticker(timeframe='h', ticker=ticker, api_key=API_KEY)
        # df4 = fetch_ticker(timeframe='h', ticker=ticker, api_key=API_KEY)

        # df1 = get_indicators(df1, indicators['daily'], params['daily'])
        df2 = get_indicators(df2, indicators['daily_2'], params['daily_2'])
        # df3 = get_indicators(df3, indicators['1hour'], params['1hour'])
        # df4 = get_indicators(df4, indicators['1hour'], params['1hour_2'])

        print(df2.columns)
        print(df2)

        subcharts(
                  [df2], 
                  ticker=ticker, 
                  show_volume=True, 
                  show_banker_RSI=False
                 )
        return

    # Scan file case - only runs if scan_file is provided
    scan_path = Path(scan_file)
    if not scan_path.exists() and not scan_path.parent.name == "scanner":
        scan_path = SCANNER_DIR / scan_path.name
    
    if not scan_path.exists():
        print(f"Error: Scan file not found at {scan_path}")
        list_scan_files(SCANNER_DIR)
        return
        
    subcharts(scan_file=scan_path)

# FETCH TICKERS -------------------------------------------

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

             # --- Multi-Timeframe Scans ---

             # 'w_QQEMODOversold_d_OBullishZone',

             # 'd_StDevOversold_h_OBSupport',
             # 'd_StDevOverbought_h_OBResistance',
             # 'd_OBSupport_h_OBSupport',
             # 'd_OBResistance_h_OBResistance',

             # 'w_bankerRSI_QQEMODOversold',
             # 'w_OBSupport',
             # 'w_bankerRSI',
             # 'w_bankerRSI_QQEMODOversold',

             # --- Single-Timeframe Scans ---

             # 'w_QQEMODBullishReversal',
             # 'w_QQEMODBearishReversal',

             # 'd_aVWAPavgBelow_OBBullish',
             # 'd_QQEMODBullishReversal',
             # 'd_QQEMODBearishReversal',
             # 'd_QQEMODOversold_OBSupport',
             # 'd_bankerRSI_QQEMODOversold',
             # 'd_aVWAPavg',
             # 'd_SMA',

             # 'h_StDevOversold_OBSupport',
             # 'h_OBSupport',
             # 'h_QQEMODBearishReversal',
             # 'h_QQEMODBearishReversal',
             'h_aVWAPavgBelow_OBBullish',

            ]

    for scan in scans:
        kwargs = {
            'criteria': scan_configs[scan]['criteria'],
            'criteria_params': scan_configs[scan]['params'],
            'scan_name': scan
        }
        run_scanner(**kwargs)

# COMMAND LINE INTERFACE (CLI) ----------------------------

# RUN 'python app.py' for HELP command list
if __name__ == "__main__": init_cli(vis, fetch, ind, scan)
