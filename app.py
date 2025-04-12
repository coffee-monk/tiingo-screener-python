from datetime import datetime
import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators
from src.data.fetch_data.fetch_data import fetch_data
from src.visualizations.subcharts import subcharts

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

# Fetch -----------------------------------------

ticker = 'SHOP' ; start_date = '2022-08-13'
# ticker = 'SPY' ; start_date = '2023-08-27'

df1 = fetch_data(time_period='h',
                ticker=ticker,
                start_date=start_date,
                api_key=API_KEY)

# df2 = fetch_data(time_period='d',
#                 ticker=ticker,
#                 start_date=start_date,
#                 api_key=API_KEY)
#
# df3 = fetch_data(time_period='h',
#                 ticker=ticker,
#                 start_date=start_date,
#                 api_key=API_KEY)
#
# df4 = fetch_data(time_period='5m',
#                 ticker=ticker,
#                 # start_date='2025-03-21',
#                 api_key=API_KEY)

# Indicators ------------------------------------

df1 = get_indicators(df1, ['aVWAP_Channel'], {'aVWAP_Channel': {'window_size': 200}})
# df2 = get_indicators(df2, ['BoS_CHoCH', 'FVG', 'OB'], {'peaks_valleys': {'window_size': 50}})
# df3 = get_indicators(df3, ['BoS_CHoCH', 'FVG', 'OB'], {'peaks_valleys': {'window_size': 150}})
# df4 = get_indicators(df4, ['BoS_CHoCH', 'FVG', 'OB'], {'peaks_valleys': {'window_size': 120}})

print(df1.shape)
print(df1.head(10))
print(df1.tail(10))

# Output/Visualization --------------------------

subcharts([df1, df1, df1, df1], ticker, show_volume=False)
