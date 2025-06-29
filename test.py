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

indicator_list = [
    # 'aVWAP', 
    # 'candle_colors', 
    # 'liquidity', 
    # 'BoS_CHoCH', 
    # 'ZScore', 
    # 'StDev', 
    # 'QQEMOD',
    # 'banker_RSI', 
    'SMA',
    # 'supertrend',
    # 'OB',
    # 'TTM_squeeze',
    # 'divergence_ATR', 
    # 'divergence_Vortex',
    # 'divergence_Fisher',
    # 'divergence_OBV',
    # 'divergence_Volume'
]

params = {
    # 'candle_colors': {'indicator_color': 'StDev', 
    #                   'custom_params': {'StDev': {'std_lookback': 4, 
    #                                               'avg_lookback': 4,
    #                                               'centreline': 'peaks_valleys_avg',
    #                                               'peaks_valleys_params': {
    #                                                   'periods': 8,
    #                                                   'max_aVWAPs': None
    #                                               }}}},
    'candle_colors': {'indicator_color': 'QQEMOD', 
                      'custom_params': {'QQEMOD': {'rsi_period': 6, 
                                                   'rsi_period2': 5,
                                                   'sf': 6,
                                                   'sf2': 5,
                                                   'qqe_factor': 3.0,
                                                   'qqe_factor2': 1.61,
                                                   'threshold': 3,
                                                   'bb_length': 10,
                                                   'bb_multi': 0.35,
                                                  }}},
    'aVWAP': { 
              'peaks_valleys': False,
              'peaks_valleys_avg': False,
              'peaks_valleys_params': { 'periods': 8, 'max_aVWAPs': None },
              'OB': True,
              'OB_avg': False,
              'OB_params': { 'periods': 21, 'max_aVWAPs': 5 },
              'gaps': False,
              'gaps_avg': False,
              'gaps_params': { 'max_aVWAPs': 10 },
              'avg_lookback': 8,
              'keep_OB_column': True,
             },
    'ZScore': {
              'centreline': 'peaks_valleys_avg', 
              'peaks_valleys_params': { 'periods': 20, 'max_aVWAPs': None }, 
              # 'gaps_params': { 'max_aVWAPs': 10 }, 
              'std_lookback': 75,
              'avg_lookback': 20,
              },
    'QQEMOD': {
              'rsi_period': 10,
              'rsi_period2': 5,
              'sf': 10,
              'sf2': 5,
              'qqe_factor': 3.0,
              'qqe_factor2': 1.5,
              'threshold': 3,
              'bb_length': 20,
              'bb_multi': 0.35,
              },
    # 'StDev': {
    #           'centreline': 'peaks_valleys_avg', 
    #           'peaks_valleys_params': { 'periods': 20, 'max_aVWAPs': None }, 
    #           # 'gaps_params': { 'max_aVWAPs': 10 }, 
    #           'std_lookback': 75,
    #           'avg_lookback': 21,
    #           },
    'SMA': {'periods': [20, 50, 100, 200]},
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

ticker = 'TD'

df1 = fetch_ticker(timeframe='d', ticker=ticker, api_key=API_KEY)

df1 = get_indicators(df1, indicator_list, params)

print(df1.columns)
print('\n')
print(df1.head(10))
print(df1.tail(10))

subcharts([df1], ticker=ticker, show_volume=True, show_banker_RSI=False, csv_loader='scanner')
