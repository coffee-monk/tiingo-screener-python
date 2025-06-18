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
from src.indicators.custom_inputs import (params_weekly, ind_weekly,  
                                          params_daily,  ind_daily,
                                          params_1hour,  ind_1hour,
                                          params_5min,   ind_1hour)

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

indicator_list = [
    'aVWAP', 
    'candle_colors', 
    'liquidity', 
    # 'BoS_CHoCH', 
    # 'ZScore', 
    # 'StDev', 
    # 'QQEMOD',
    # 'banker_RSI', 
    # 'SMA',
    # 'supertrend',
    'OB',
    'TTM_squeeze',
    # 'divergence_ATR', 
    'divergence_Vortex',
    'divergence_Fisher',
    'divergence_OBV',
    'divergence_Volume'
]

params = {
    'candle_colors': {'indicator_color': 'StDev', 
                      'custom_params': {'StDev': {'std_lookback': 50, 
                                                  'avg_lookback': 5,
                                                  'centreline': 'peaks_valleys_avg',
                                                  'peaks_valleys_params': {
                                                      'periods': 21,
                                                      'max_aVWAPs': None
                                                  }}}},
    'aVWAP': { 
              'peaks_valleys': False,
              'peaks_valleys_avg': True,
              'peaks_valleys_params': { 'periods': 21, 'max_aVWAPs': None },
              'OB': True,
              'OB_avg': False,
              'OB_params': { 'periods': 21, 'max_aVWAPs': 5 },
              'gaps': False,
              'gaps_avg': False,
              'gaps_params': { 'max_aVWAPs': 10 },
              'avg_lookback': 5,
              'keep_OB_column': True,
             },
    'ZScore': {
              'centreline': 'peaks_valleys_avg', 
              'peaks_valleys_params': { 'periods': 20, 'max_aVWAPs': None }, 
              # 'gaps_params': { 'max_aVWAPs': 10 }, 
              'std_lookback': 75,
              'avg_lookback': 20,
              },
    'StDev': {
              'centreline': 'peaks_valleys_avg', 
              'peaks_valleys_params': { 'periods': 20, 'max_aVWAPs': None }, 
              # 'gaps_params': { 'max_aVWAPs': 10 }, 
              'std_lookback': 75,
              'avg_lookback': 21,
              },
    'SMA': {'periods': [21]},
    'TTM_squeeze': {'bb_length': 20, 
                    'bb_std_dev': 2.0, 
                    'kc_length': 20, 
                    'kc_mult': 1.5, 
                    'use_true_range': True},
    # 'divergence_ATR':    {'period':  80, 'lookback': 30},
    'divergence_OBV':    {'period': 100, 'lookback': 40},
    'divergence_Volume': {'period': 100, 'lookback': 40},
    'divergence_Fisher': {'period': 100, 'lookback': 40},
    'divergence_Vortex': {'period': 100, 'lookback': 40},
}

# SUBCHARTS -----------------------------------------------

ticker = 'AAPL'

df1 = fetch_ticker(timeframe='d', ticker=ticker, api_key=API_KEY)

# df1 = fetch_ticker(timeframe='w', ticker=ticker, api_key=API_KEY)
# df2 = fetch_ticker(timeframe='d', ticker=ticker, api_key=API_KEY)
# df3 = fetch_ticker(timeframe='h', ticker=ticker, api_key=API_KEY)
# df4 = fetch_ticker(timeframe='5min', ticker=ticker, api_key=API_KEY)

df1 = get_indicators(df1, indicator_list, params)

# df1 = get_indicators(df1, ind_weekly, params_weekly)
# df2 = get_indicators(df2, ind_daily,  params_daily)
# df3 = get_indicators(df3, ind_1hour,  params_1hour)
# df4 = get_indicators(df4, ind_5min,   params_5min)

# print(df1.columns)
# print('\n')
# print(df1.head(10))
# print(df1.tail(10))

# subcharts([df1, df2, df3, df4], ticker=ticker, show_volume=True, show_banker_RSI=False, csv_loader='scanner')
subcharts([df1], ticker=ticker, show_volume=True, show_banker_RSI=False, csv_loader='indicators')

# FETCH TICKERS -------------------------------------------

# fetch_tickers(['weekly', 'daily', '1hour', '5min'], api_key=API_KEY)

# INDICATORS ---------------------------------------------

# run_indicators(ind_weekly, params_weekly, "weekly")
# run_indicators(ind_daily, params_daily, "daily")
# run_indicators(ind_1hour, params_1hour, "1hour")
# run_indicators(ind_5min, params_5min, "5min")

# SCANNER ------------------------------------------------

# run_scanner(['TTM_squeeze'])
# run_scanner(['QQEMOD_overbought'])

# run_scanner(
#             { 
#              # 'weekly': ['OB_bullish'], 
#              'daily':  ['OB_bullish'],
#              '1hour': ['OB_bullish_below_aVWAP'], 
#             }, 
#             logic='AND'
#            )
