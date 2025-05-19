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
from src.visualization.chart_browser import chart_browser

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

indicator_list = [
    'aVWAP', 
    # 'candle_colors', 
    # 'liquidity', 
    # 'ZScore', 
    # 'QQEMOD',
    # 'banker_RSI', 
    # 'SMA',
    # 'OB',
    # 'divergence_ATR', 
    # 'divergence_Vortex', 
    # 'divergence_Fisher', 
    # 'divergence_OBV', 
    # 'divergence_Volume'
]

params = {
    # 'SMA': {'periods': [50, 200]},
    # 'divergence_ATR':    {'period':  80, 'lookback': 30},
    # 'divergence_OBV':    {'period': 100, 'lookback': 40},
    # 'divergence_Volume': {'period': 100, 'lookback': 40},
    # 'divergence_Fisher': {'period': 100, 'lookback': 40},
    # 'divergence_Vortex': {'period': 100, 'lookback': 40},
}

# Example Code ----------------------------------------------------------------

ticker = 'AAPL'

df1 = fetch_ticker(timeframe='weekly', ticker=ticker, api_key=API_KEY)
df2 = fetch_ticker(timeframe='daily', ticker=ticker, api_key=API_KEY)
df3 = fetch_ticker(timeframe='hour', ticker=ticker, api_key=API_KEY)
df4 = fetch_ticker(timeframe='5min', ticker=ticker, api_key=API_KEY)

df1 = get_indicators(df1, indicator_list, params)
df2 = get_indicators(df2, indicator_list, params)
df3 = get_indicators(df3, indicator_list, params)
df4 = get_indicators(df4, indicator_list, params)

print(df1.columns)
print('\n')
print(df1.head(10))
print(df1.tail(10))

subcharts([df1, df2, df3, df4], ticker=ticker, show_volume=False)

# fetch_tickers(['weekly', 'daily', '1hour', '5min'], api_key=API_KEY)

# run_indicators(indicator_list, params)

# run_scanner('OB_bullish')

# run_scanner({
#             'day': 'ZScore_oversold', 
#             # 'hour': 'banker_RSI', 
#             })

# subcharts([df1, df2, df3, df4])

# subcharts_data(
#                'AMZN', 
#                data_folder='indicators'
#                )
