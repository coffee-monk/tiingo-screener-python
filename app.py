from datetime import datetime
import pandas as pd
import numpy as np
from src.indicators.get_indicators import get_indicators
from src.data.fetch_data.fetch_data import fetch_data
# from src.visualizations.visualization_test import visualization
# from src.data.fetch_data.fetch_data_test import fetch_data
# from src.visualizations.visualization import visualization
from src.visualizations.subcharts import subcharts

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

# Fetch -----------------------------------------

ticker = 'SPY'
# start_date = '2020-03-10' # BTCUSD cycle low
start_date = '2022-01-01'

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
                start_date='2025-01-01',
                api_key=API_KEY)

df4 = fetch_data(time_period='5m',
                ticker=ticker,
                # start_date='2025-03-21',
                api_key=API_KEY)

# Indicators ------------------------------------

df1 = get_indicators(df1, ['peaks_valleys', 'gaps'], {'peaks_valleys': {'window_size': 100}})
df2 = get_indicators(df2, ['peaks_valleys', 'gaps'], {'peaks_valleys': {'window_size': 100}})
df3 = get_indicators(df3, ['peaks_valleys', 'gaps'], {'peaks_valleys': {'window_size': 100}})
df4 = get_indicators(df4, ['peaks_valleys', 'gaps'], {'peaks_valleys': {'window_size': 500}})

# Output/Visualization --------------------------

subcharts([df1, df2, df3, df4], ticker)
# visualization(df1, 'aVWAP_channel')
