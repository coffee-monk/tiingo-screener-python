from datetime import datetime
import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators
from src.data.fetch_data.fetch_data import fetch_data
from src.visualization.subcharts import subcharts

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

# Fetch -----------------------------------------

ticker = 'BTCUSD' ; start_date = '2025-01-01'
# ticker = 'SPY' ; start_date = '2023-08-27'

df1 = fetch_data(time_period='d',
                 ticker=ticker,
                 # start_date=start_date,
                 api_key=API_KEY)

# df2 = fetch_data(time_period='h',
#                  ticker=ticker,
#                  start_date=start_date,
#                  api_key=API_KEY)
#
# df3 = fetch_data(time_period='h',
#                  ticker=ticker,
#                  # start_date=start_date,
#                  api_key=API_KEY)
#
# df4 = fetch_data(time_period='15min',
#                  ticker=ticker,
#                  # start_date='2025-03-21',
#                  api_key=API_KEY)

# Indicators ------------------------------------

df1 = get_indicators(df1, ['divergence_Stochastic'])
# df1 = get_indicators(df1, ['aVWAP', 'candle_colors', 'liquidity', 'banker_RSI',
#                            # 'supertrend',
#                            # 'divergence_RSI',
#                            # 'divergence_MACD',
#                            # 'divergence_Momentum',
#                            'divergence_ATR', 'divergence_Vortex', 'divergence_Fisher', 'divergence_OBV', 'divergence_Volume'
#                            ], 
#                            {
#                            'divergence_ATR':    {'period': 80, 'lookback': 30},
#                            'divergence_OBV':    {'period': 100, 'lookback': 40},
#                            'divergence_Volume': {'period': 100, 'lookback': 40},
#                            'divergence_Fisher': {'period': 100, 'lookback': 40},
#                            'divergence_Vortex': {'period': 100, 'lookback': 40},
#                            }
#                            )

# df2 = get_indicators(df2, ['aVWAP',
#                            'candle_colors',
#                            'liquidity',
#                            'banker_RSI',
#                            # 'supertrend',
#                            # 'divergence_RSI',
#                            # 'divergence_ATR',
#                            # 'divergence_MACD',
#                            # 'divergence_Momentum',
#                            'divergence_Vortex',
#                            'divergence_Fisher',
#                            'divergence_OBV',
#                            'divergence_Volume'
#                            ], 
#                            {
#                            'divergence_OBV': {'obv_period': 100, 'lookback': 40},
#                            'divergence_Volume': {'volume_period': 100, 'lookback': 40},
#                            'divergence_Fisher': {'fisher_period': 100, 'lookback': 40},
#                            'divergence_Vortex': {'period': 100, 'lookback': 40},
#                            }
#                            )

# df2 = get_indicators(df2, ['aVWAP', 'candle_colors', 'liquidity', 'SMA'])
# df3 = get_indicators(df3, ['aVWAP', 'candle_colors', 'liquidity', 'SMA'])
# df4 = get_indicators(df4, ['aVWAP', 'candle_colors', 'liquidity', 'SMA'])

print('\n')
print(df1.columns)
print(df1.head(10))
print(df1.tail(10))
print('\n')

# Output/Visualization --------------------------

subcharts([df1], ticker, show_volume=False)
# subcharts([df1, df2, df3, df4], ticker, show_volume=False)
