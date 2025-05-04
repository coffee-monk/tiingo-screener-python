import os
import pandas as pd
from datetime import datetime
from src.indicators.get_indicators import get_indicators
from src.indicators.run_indicators import run_indicators
from src.fetch_data.fetch_tickers import fetch_tickers

API_KEY = '9807b06bf5b97a8b26f5ff14bff18ee992dfaa13'

TIMEFRAMES = ['week', 'day', 'hour', '15min']

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

# fetch_tickers(TIMEFRAMES, API_KEY=API_KEY)

run_indicators(indicator_list)
