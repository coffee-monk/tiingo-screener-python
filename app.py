import os
import time
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
from config.CLI import init_cli
from config.settings import SCANNER_DIR
from config.data_manager import dm
from config.scan_lists import scan_lists

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

# VISUALIZATION ------------------------------------------

def vis(scan_file=None, ticker=None, timeframe=None, version=None):

    if not scan_file:

        if not ticker: ticker = 'BTCUSD'

        if timeframe:

            df = fetch_ticker(timeframe=timeframe, ticker=ticker, api_key=API_KEY)
            ind_conf_ver = f"{timeframe}_{version}" if version else f"{timeframe}"
            df = get_indicators(df, indicators[ind_conf_ver], params[ind_conf_ver])

            subcharts(
                      [df], 
                      ticker=ticker, 
                      show_volume=False, 
                      show_banker_RSI=True
                     )
            return

        # df1 = fetch_ticker(timeframe='w',  ticker=ticker, api_key=API_KEY)
        df2 = fetch_ticker(timeframe='d',  ticker=ticker, api_key=API_KEY)
        # df3 = fetch_ticker(timeframe='4h', ticker=ticker, api_key=API_KEY)
        # df4 = fetch_ticker(timeframe='h',  ticker=ticker, api_key=API_KEY)

        # df1 = get_indicators(df1, indicators['weekly_2'], params['weekly_2'])
        df2 = get_indicators(df2, indicators['daily_2'],  params['daily_2'])
        # df3 = get_indicators(df3, indicators['4hour_2'],  params['4hour_2'])
        # df4 = get_indicators(df4, indicators['1hour_2'],  params['1hour_2'])

        subcharts(
                  [df2],
                  ticker=ticker,
                  show_volume=False,
                  show_banker_RSI=True
                 )
        return

    scan_path = Path(scan_file)
    if not scan_path.exists():
        scan_path = SCANNER_DIR / scan_path.name

    if not scan_path.exists():
        print(f"Error: Scan file not found at {scan_path}")
        dm.list_scans()
        return

    subcharts(
              scan_file=scan_path,
              show_volume=False,
              show_banker_RSI=False
             )

# FETCH TICKERS -------------------------------------------

def fetch():

    fetch_tickers(['weekly'], api_key=API_KEY)
    fetch_tickers(['daily'],  api_key=API_KEY)
    fetch_tickers(['4hour'],  api_key=API_KEY)
    fetch_tickers(['1hour'],  api_key=API_KEY)
    # fetch_tickers(['5min'],   api_key=API_KEY)

# INDICATORS ----------------------------------------------

def ind(ind_conf=None):

    match ind_conf:

        case 'ind_conf_1':
            run_indicators(indicators['weekly_1'], params['weekly_1'], "weekly")
            run_indicators(indicators['daily_1'],  params['daily_1'],  "daily")
            run_indicators(indicators['4hour_1'],  params['4hour_1'],  "4hour")
            run_indicators(indicators['1hour_1'],  params['1hour_1'],  "1hour")

        case 'ind_conf_2':
            run_indicators(indicators['weekly_2'], params['weekly_2'], "weekly")
            run_indicators(indicators['daily_2'],  params['daily_2'],  "daily")
            run_indicators(indicators['4hour_2'],  params['4hour_2'],  "4hour")
            run_indicators(indicators['1hour_2'],  params['1hour_2'],  "1hour")

        case 'ind_conf_3':
            run_indicators(indicators['weekly_3'], params['weekly_3'], "weekly")
            run_indicators(indicators['daily_3'],  params['daily_3'],  "daily")
            run_indicators(indicators['4hour_3'],  params['4hour_3'],  "4hour")
            run_indicators(indicators['1hour_3'],  params['1hour_3'],  "1hour")

        case 'ind_conf_4':
            run_indicators(indicators['weekly_4'], params['weekly_4'], "weekly")
            run_indicators(indicators['daily_4'],  params['daily_4'],  "daily")
            run_indicators(indicators['4hour_4'],  params['4hour_4'],  "4hour")
            run_indicators(indicators['1hour_4'],  params['1hour_4'],  "1hour")

# SCANNER -------------------------------------------------

def scan(scan_list='scan_list_2'):

    scans = scan_lists[scan_list]

    for scan in scans:
        kwargs = {
            'criteria': scan_configs[scan]['criteria'],
            'criteria_params': scan_configs[scan]['params'],
            'scan_name': scan
        }
        # print(kwargs)
        run_scanner(**kwargs)

# FULL RUN ------------------------------------------------

def full_run(fetch, ind, scan) -> None:
    """Standard full run pipeline"""

    start_time = time.time() # Start timer

    # FETCH

    dm.clear_all_buffers()
    dm.delete_all_versions(dm.tickers_dir)
    dm.delete_all_versions(dm.indicators_dir)
    dm.delete_all_versions(dm.scanner_dir)

    fetch()

    # INDICATORS

    ind('ind_conf_1')
    dm.save_indicators('ind_conf_1')
    dm.clear_buffer(dm.indicators_dir)
    
    ind('ind_conf_2')
    dm.save_indicators('ind_conf_2')
    dm.clear_buffer(dm.indicators_dir)
    
    ind('ind_conf_3')
    dm.save_indicators('ind_conf_3')
    dm.clear_buffer(dm.indicators_dir)
    
    ind('ind_conf_4')
    dm.save_indicators('ind_conf_4')
    dm.clear_buffer(dm.indicators_dir)

    # SCANNER

    # scan(scan_lists['scan_list_1'])
    # dm.save_scans('ind_conf_1')
    # dm.clear_buffer(dm.scanner_dir)
    #
    # scan(scan_lists['scan_list_1'])
    # dm.save_scans('ind_conf_2')
    # dm.clear_buffer(dm.scanner_dir)
    #
    # scan(scan_lists['scan_list_1'])
    # dm.save_scans('ind_conf_3')
    # dm.clear_buffer(dm.scanner_dir)

    # COMPLETE

    total_time = dm.format_duration(time.time() - start_time)
    print(f"\n✅ Standard full run completed in {total_time}")

# COMMAND LINE INTERFACE (CLI) ----------------------------

# RUN 'python app.py' for HELP command list
if __name__ == "__main__": init_cli(vis, fetch, ind, scan, full_run)
