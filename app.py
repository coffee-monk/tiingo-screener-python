import os
import argparse
import pandas as pd
from datetime import datetime
from src.indicators.get_indicators import get_indicators
from src.indicators.run_indicators import run_indicators
from src.fetch_data.fetch_tickers import fetch_tickers
from src.fetch_data.fetch_ticker import fetch_ticker
from src.scanner.scanner import run_scanner
from src.visualization.subcharts import subcharts
from src.visualization.subcharts import subcharts
from src.scanner.custom_inputs import scan_configs
from src.indicators.custom_inputs import ind_configs

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

indicators = ind_configs['indicators']
params     = ind_configs['params']

# SUBCHARTS -----------------------------------------------

def vis(): 

    ticker = 'VRN'

    # df1 = fetch_ticker(timeframe='w', ticker=ticker, api_key=API_KEY)
    df2 = fetch_ticker(timeframe='d', ticker=ticker, api_key=API_KEY)
    # df3 = fetch_ticker(timeframe='h', ticker=ticker, api_key=API_KEY)
    # df4 = fetch_ticker(timeframe='5min', ticker=ticker, api_key=API_KEY)

    # df1 = get_indicators(df1, indicators['weekly'], params['weekly'])
    df2 = get_indicators(df2, indicators['daily'], params['daily'])
    # df3 = get_indicators(df3, indicators['1hour'], params['1hour'])
    # df4 = get_indicators(df4, indicators['5min'], params['5min'])

    # print(df1.columns)
    # print('\n')
    # print(df1.head(10))
    # print(df1.tail(10))

    subcharts([df2], ticker=ticker, 
              show_volume=True, show_banker_RSI=False, csv_loader='scanner')
    # subcharts([df1, df2, df3, df4], ticker=ticker, 
    #           show_volume=True, show_banker_RSI=False, csv_loader='scanner')

# FETCH TICKERS -------------------------------------------

def fetch():

    fetch_tickers(['weekly'], api_key=API_KEY)
    fetch_tickers(['daily'],  api_key=API_KEY)
    fetch_tickers(['1hour'],  api_key=API_KEY)
    fetch_tickers(['5min'],   api_key=API_KEY)

# INDICATORS ---------------------------------------------

def ind():

    # run_indicators(indicators['weekly'], params['weekly'], "weekly")
    # run_indicators(indicators['daily'],  params['daily'],  "daily")
    # run_indicators(indicators['1hour'],  params['1hour'],  "1hour")
    # run_indicators(indicators['5min'],   params['5min'],   "5min")

    run_indicators(['SMA', 'candle_colors'], params['weekly'], "weekly")
    run_indicators(['SMA', 'candle_colors'],  params['daily'],  "daily")
    run_indicators(['SMA', 'candle_colors'],  params['1hour'],  "1hour")
    run_indicators(['SMA', 'candle_colors'],   params['5min'],   "5min")

# SCANNER ------------------------------------------------

def scan():

    scans = [
        # 'd_supertrendBullish_QQEMODOversold',
        # 'd_bankerRSI_QQEMODOversold',
        # 'dh_StDevOversold_OBSupport',
        # 'd_QQEMODOversold_OBSupport'
        'd_SMAAbove'
    ]

    for scan in scans:
        kwargs = {
            'criteria': scan_configs[scan]['criteria'],
            'criteria_params': scan_configs[scan]['params'],
            'scan_name': scan
        }
        run_scanner(**kwargs)

# TERMINAL COMMANDS ///////////////////////////////////////

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--vis', action='store_true', help='Run SMA scanner')
    parser.add_argument('--fetch', action='store_true', help='Run liquidity scanner')
    parser.add_argument('--ind', action='store_true', help='Run liquidity scanner')
    parser.add_argument('--scan', action='store_true', help='Run volume scanner')

    args = parser.parse_args()

    if args.vis: vis()
    elif args.fetch: fetch()
    elif args.ind: ind()
    elif args.scan: scan()
    else: print("Please specify: --vis, --fetch, --ind, --scan")
