import os
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

ticker = 'EQX'

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

subcharts([df2], ticker=ticker, show_volume=True, show_banker_RSI=False, csv_loader='scanner')
# subcharts([df1, df2, df3, df4], 
#             ticker=ticker, show_volume=True, show_banker_RSI=False, csv_loader='scanner')

# FETCH TICKERS -------------------------------------------

# fetch_tickers(['weekly'], api_key=API_KEY)
# fetch_tickers(['daily'],  api_key=API_KEY)
# fetch_tickers(['1hour'],  api_key=API_KEY)
# fetch_tickers(['5min'],   api_key=API_KEY)

# INDICATORS ---------------------------------------------

# run_indicators(indicators['weekly'], params['weekly'], "weekly")
# run_indicators(indicators['daily'],  params['daily'],  "daily")
# run_indicators(indicators['1hour'],  params['1hour'],  "1hour")
# run_indicators(indicators['5min'],   params['5min'],   "5min")

# SCANNER ------------------------------------------------

# run_scanner('TTM_squeeze')
# run_scanner(['QQEMOD_overbought', 'StDev'])

# run_scanner(
#             criteria={ 
#              # 'weekly': ['TTM_squeeze'], 
#              'daily':  ['StDev'],
#              # '1hour': ['OB_bullish_support'], 
#              # '5min': ['OB_bullish_below_aVWAP'], 
#             }, 
#             logic='AND',
#             criteria_params={
#                 'StDev': {
#                     'daily': {
#                         'threshold': 2,
#                         'mode': 'overbought'
#                         }
#                     }
#                 }
#            )

# run_scanner(criteria=scan_configs['d_supertrendBullish_QQEMODOversold']['criteria'],
#             scan_name='d_supertrendBullish_QQEMODOversold')

# run_scanner(criteria=scan_configs['d_bankerRSI_QQEMODOversold']['criteria'],
#             scan_name='d_bankerRSI_QQEMODOversold')

# run_scanner(criteria=scan_configs['dh_StDevOversold_OBBSupport']['criteria'],
#             criteria_params=scan_configs['dh_StDevOversold_OBBSupport']['params'],
#             scan_name='dh_StDevOversold_OBBSupport')

# run_scanner(criteria=scan_configs['d_QQEMODOversold_OBSupport']['criteria'],
#             criteria_params=scan_configs['d_QQEMODOversold_OBSupport']['params'],
#             scan_name='d_QQEMODOversold_OBSupport')

# run_scanner(criteria=scan_configs['wd_supertrendBearish_OBBullishZone']['criteria'],
#             scan_name='wd_supertrendBearish_OBBullishZone')
