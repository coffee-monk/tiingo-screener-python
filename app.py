import os
import pandas as pd
from datetime import datetime
from src.indicators.get_indicators import get_indicators
from src.indicators.run_indicators import run_indicators
from src.fetch_data.fetch_tickers import fetch_tickers
from src.fetch_data.fetch_ticker import fetch_ticker
from src.scanner.scanner import run_scanner
from src.visualization.subcharts import subcharts

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

indicator_list = [
    # 'aVWAP', 
    'candle_colors', 
    # 'liquidity', 
    # 'BoS_CHoCH', 
    # 'ZScore', 
    # 'StDev', 
    # 'QQEMOD',
    # 'banker_RSI', 
    # 'SMA',
    # 'supertrend',
    # 'OB',
    # 'divergence_ATR', 
    # 'divergence_Vortex',
    # 'divergence_Fisher',
    # 'divergence_OBV',
    # 'divergence_Volume'
]

params = {
    'aVWAP': { 
              'peaks_valleys': False,
              'peaks_valleys_avg': False,
              'peaks_valleys_params': { 'periods': 20, 'max_aVWAPs': None },
              'OB': True,
              'OB_avg': False,
              'OB_params': { 'periods': 20, 'max_aVWAPs': 5 },
              'gaps': False,
              'gaps_avg': False,
              'gaps_params': { 'max_aVWAPs': 10 },
              'avg_lookback': 20,
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
              'avg_lookback': 20,
              },
    'candle_colors': {'indicator_color': 'banker_RSI'},
    # 'SMA': {'periods': [200]},
    # 'divergence_ATR':    {'period':  80, 'lookback': 30},
    'divergence_OBV':    {'period': 100, 'lookback': 40},
    'divergence_Volume': {'period': 100, 'lookback': 40},
    'divergence_Fisher': {'period': 100, 'lookback': 40},
    'divergence_Vortex': {'period': 100, 'lookback': 40},
}

# Example Code ---------------------------------------------------------------

ticker = 'ESI'

df1 = fetch_ticker(timeframe='d', ticker=ticker, api_key=API_KEY)
df2 = fetch_ticker(timeframe='daily', ticker=ticker, api_key=API_KEY)
df3 = fetch_ticker(timeframe='hourly', ticker=ticker, api_key=API_KEY)
df4 = fetch_ticker(timeframe='5min', ticker=ticker, api_key=API_KEY)

df1 = get_indicators(df1, indicator_list, params)
df2 = get_indicators(df2, indicator_list, params)
df3 = get_indicators(df3, indicator_list, params)
df4 = get_indicators(df4, indicator_list, params)

# print(df1.columns)
# print('\n')
# print(df1.head(10))
# print(df1.tail(10))

subcharts([df1, df2, df3, df4], ticker=ticker, show_volume=True, show_banker_RSI=False, csv_loader='scanner')

# fetch_tickers(['weekly', 'daily', '1hour'], api_key=API_KEY)

# run_indicators(indicator_list, params)

# run_scanner(['div_vortex_bullish'])
# run_scanner(['QQEMOD_overbought'])

# run_scanner(
#             { 
#              'weekly': ['OB_bullish', 'banker_RSI'], 
#              'daily':  ['OB_bullish', 'banker_RSI'],
#              'hourly': ['banker_RSI'], 
#             }, 
#             logic='AND'
#            )
