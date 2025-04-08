from datetime import datetime
import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators
from src.data.fetch_data.fetch_data import fetch_data
from src.visualizations.subcharts import subcharts

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

# Fetch -----------------------------------------

ticker = 'SHOP' ; start_date = '2022-08-13'

df1 = fetch_data(time_period='w',
                ticker=ticker,
                start_date=start_date,
                api_key=API_KEY)

df2 = fetch_data(time_period='d',
                ticker=ticker,
                start_date=start_date,
                api_key=API_KEY)

df3 = fetch_data(time_period='h',
                ticker=ticker,
                start_date=start_date,
                api_key=API_KEY)

df4 = fetch_data(time_period='5m',
                ticker=ticker,
                # start_date='2025-03-21',
                api_key=API_KEY)

# Indicators ------------------------------------

# df = get_indicators(df, ['FVG'])

df1 = get_indicators(df1, ['FVG', 'SMA', 'peaks_valleys'], {'peaks_valleys': {'window_size': 10}})
df2 = get_indicators(df2, ['FVG', 'SMA', 'peaks_valleys'], {'peaks_valleys': {'window_size': 50}})
df3 = get_indicators(df3, ['FVG', 'SMA', 'peaks_valleys'], {'peaks_valleys': {'window_size': 150}})
df4 = get_indicators(df4, ['FVG', 'SMA', 'peaks_valleys'], {'peaks_valleys': {'window_size': 120}})

# df1 = get_indicators(df1, ['FVG', 'peaks_valleys'], {'peaks_valleys': {'window_size': 10}})
# df2 = get_indicators(df2, ['FVG', 'peaks_valleys'], {'peaks_valleys': {'window_size': 50}})
# df3 = get_indicators(df3, ['FVG', 'peaks_valleys'], {'peaks_valleys': {'window_size': 150}})
# df4 = get_indicators(df4, ['FVG', 'peaks_valleys'], {'peaks_valleys': {'window_size': 120}})

# print(df1.columns)
# print(df1.head(10))
# print(df1.tail(10))

# Output/Visualization --------------------------

subcharts([df1, df2, df3, df4], ticker, show_volume=False)
