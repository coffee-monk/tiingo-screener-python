from datetime import datetime, timedelta
import pandas as pd
import requests
from tiingo import TiingoClient

def fetch_ticker(timeframe='daily', ticker='BTCUSD', start_date=None, end_date=None, api_key='Tiingo-API-Key'):
    """
    Fetch historical price data for a given ticker and time period.

    Parameters:
        timeframe (str): Time period for the data (e.g., 'daily', 'hourly', '1min').
        ticker (str): Ticker symbol (e.g., 'BTCUSD').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        api_key (str): Tiingo API key.

    Returns:
        pd.DataFrame: DataFrame containing the fetched data.
    """
    # Set default end_date to today if not provided
    if not end_date: end_date = datetime.now().date()

    # Initialize Tiingo client
    client = TiingoClient({'api_key': api_key, 'session': True})
    headers = {'Content-Type': 'application/json'}

    # Define time period configurations
    timeframe_config = {
        'daily':     {   'frequency':  'daily', 'default_timedelta': None},
        'day':       {   'frequency':  'daily', 'default_timedelta': None},
        '1day':      {   'frequency':  'daily', 'default_timedelta': None},
        'd':         {   'frequency':  'daily', 'default_timedelta': None},
        'weekly':    {   'frequency': 'weekly', 'default_timedelta': None},
        '1week':     {   'frequency': 'weekly', 'default_timedelta': None},
        'week':      {   'frequency': 'weekly', 'default_timedelta': None},
        'w':         {   'frequency': 'weekly', 'default_timedelta': None},
        '4hour':     {'resampleFreq':  '4hour', 'default_timedelta': timedelta(hours=15000)},
        '4h':        {'resampleFreq':  '4hour', 'default_timedelta': timedelta(hours=15000)},
        'hourly':    {'resampleFreq':  '1hour', 'default_timedelta': timedelta(hours=5000)},
        'hour':      {'resampleFreq':  '1hour', 'default_timedelta': timedelta(hours=5000)},
        '1hour':     {'resampleFreq':  '1hour', 'default_timedelta': timedelta(hours=5000)},
        'h':         {'resampleFreq':  '1hour', 'default_timedelta': timedelta(hours=5000)},
        'minute':    {'resampleFreq':   '1min', 'default_timedelta': timedelta(hours=100)},
        '1min':      {'resampleFreq':   '1min', 'default_timedelta': timedelta(hours=100)},
        'min':       {'resampleFreq':   '1min', 'default_timedelta': timedelta(hours=100)},
        '1m':        {'resampleFreq':   '1min', 'default_timedelta': timedelta(hours=100)},
        'm':         {'resampleFreq':   '1min', 'default_timedelta': timedelta(hours=100)},
        '5minutes':  {'resampleFreq':   '5min', 'default_timedelta': timedelta(hours=100)},
        '5min':      {'resampleFreq':   '5min', 'default_timedelta': timedelta(hours=100)},
        '5m':        {'resampleFreq':   '5min', 'default_timedelta': timedelta(hours=100)},
        '15minutes': {'resampleFreq':  '15min', 'default_timedelta': timedelta(hours=3000)},
        '15min':     {'resampleFreq':  '15min', 'default_timedelta': timedelta(hours=3000)},
        '15m':       {'resampleFreq':  '15min', 'default_timedelta': timedelta(hours=3000)},
    }

    # Get the configuration for the specified time period
    config = timeframe_config.get(timeframe.lower())
    if not config:
        raise ValueError(f"Unsupported time period: {timeframe}")

    # Calculate start_date if not provided
    if start_date == None and config['default_timedelta']:
        start_date = (datetime.now() - config['default_timedelta']).strftime('%Y-%m-%d')
    elif start_date == None:
        start_date = '2022-01-01'  # Default start date

    # Fetch data (Tiingo API) -------------------------------------------------

    # fetch daily/weekly data
    if 'frequency' in config:
        data = client.get_ticker_price(ticker, startDate=start_date, endDate=end_date, frequency=config['frequency'])
        df = create_df(data, config['frequency'])
        df.attrs['timeframe'] = config['frequency']

    else:
        # fetch intraday stock data
        try:
            api_url = f"https://api.tiingo.com/iex/{ticker}/prices"
            params = {
                'startDate': start_date,
                'endDate': end_date,
                'resampleFreq': config['resampleFreq'],
                'columns': 'open,high,low,close,volume',
                'token': api_key
            }
            response = requests.get(api_url, headers=headers, params=params)
            data = response.json()
            df = create_df(data, config['resampleFreq'])
            df.attrs['timeframe'] = config['resampleFreq']

        # fetch intraday crypto data
        except ValueError:
            api_url = f"https://api.tiingo.com/tiingo/crypto/prices"
            params = {
                'tickers': {ticker},
                'startDate': start_date,
                'endDate': end_date,
                'resampleFreq': config['resampleFreq'],
                'columns': 'open,high,low,close,volume',
                'token': api_key
            }
            response = requests.get(api_url, headers=headers, params=params)
            data = response.json()
            data = data[0]['priceData']
            df = create_df(data, config['resampleFreq'])
            df = df.drop(columns=['volumeNotional', 'tradesDone'])
            df.attrs['timeframe'] = config['resampleFreq']

    return df

def create_df(data, timeframe='daily'):

    df = pd.DataFrame(data)

    match timeframe:

        case 'daily'|'1day'|'d'|'weekly'|'1week'|'w':

            df.rename(columns={
                'adjLow': 'Low',
                'adjHigh': 'High',
                'adjClose': 'Close',
                'adjOpen': 'Open',
                'adjVolume': 'Volume'
            }, inplace=True)

            columns_to_drop = ['close', 'high', 'low', 'open', 'volume', 'splitFactor', 'divCash']
            df = df.drop(columns=columns_to_drop)

        case 'hourly'|'1hour'|'h'|'4hour'|'4h'|'15minutes'|'15min'|'15m'|'5minutes'|'5min'|'5m'|'min'|'m'|'minute'|'1min'|'1m':

            df.rename(columns={
                'low': 'Low',
                'high': 'High',
                'close': 'Close',
                'open': 'Open',
                'volume': 'Volume',
            }, inplace=True)

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True) 

    return df
