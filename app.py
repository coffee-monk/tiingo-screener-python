import os
import pandas as pd
from datetime import datetime
from src.indicators.get_indicators import get_indicators
from src.indicators.run_indicators import run_indicators
from src.fetch_data.fetch_tickers import fetch_tickers
from src.fetch_data.fetch_ticker import fetch_ticker
from src.scanner.scanner import run_scanner
from src.visualization.subcharts import subcharts
from src.visualization.subcharts_data import subcharts_data

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

indicator_list = [
    'aVWAP', 
    'candle_colors', 
    'liquidity', 
    'banker_RSI', 
    'SMA',
    'divergence_ATR', 
    'divergence_Vortex', 
    'divergence_Fisher', 
    'divergence_OBV', 
    'divergence_Volume'
]

params = {
    'divergence_ATR':    {'period':  80, 'lookback': 30},
    'divergence_OBV':    {'period': 100, 'lookback': 40},
    'divergence_Volume': {'period': 100, 'lookback': 40},
    'divergence_Fisher': {'period': 100, 'lookback': 40},
    'divergence_Vortex': {'period': 100, 'lookback': 40},
}

# Example Code ----------------------------------------------------------------

# df1 = fetch_ticker(timeframe='weekly', ticker='A', api_key=API_KEY)
# df2 = fetch_ticker(timeframe='daily', ticker='A', api_key=API_KEY)
# df3 = fetch_ticker(timeframe='4hour', ticker='A', api_key=API_KEY)
# df4 = fetch_ticker(timeframe='hour', ticker='A', api_key=API_KEY)
# subcharts([df1, df2, df3, df4], ticker='A', show_volume=False)

# fetch_tickers(['week', 'day', 'hour', '15min'], api_key=API_KEY)

# run_indicators(indicator_list, params)

# run_scanner()

# run_scanner({
#             'day': 'banker_RSI', 
#             'week': 'banker_RSI', 
#             })

# subcharts_data('A')

# subcharts([df1, df2, df3, df4])
