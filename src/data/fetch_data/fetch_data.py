# from pprint import pprint
# import requests
# from tiingo import TiingoClient
# from src.data.fetch_data.utils.create_df import create_df
# from datetime import datetime, timedelta
#
# def fetch_data(time_period='daily', ticker='BTCUSD', start_date='2024-01-01', end_date=datetime.now().date(), api_key='Tiingo-API-Key'):
#
#     client = TiingoClient({ 'api_key': api_key, 'session': True  })
#
#     headers = { 'Content-Type': 'application/json' }
#
#     match time_period:
#
#         case 'daily'|'1day'|'d':
#
#             data = client.get_ticker_price(ticker, startDate=start_date, endDate=end_date, frequency='daily')
#
#         case 'weekly'|'1week'|'w':
#
#             data = client.get_ticker_price(ticker, startDate=start_date, endDate=end_date, frequency='weekly')
#
#         case 'hourly'|'1hour'|'h':
#
#             api_url = f"https://api.tiingo.com/iex/{ticker}/prices"
#             start_date = end_date-timedelta(hours=2000)
#             start_date = start_date.strftime('%Y-%m-%d')
#
#             params = {
#                 'startDate': start_date, # start_date
#                 'endDate': end_date, # end_date,
#                 'resampleFreq': '1hour',
#                 'columns': 'open,high,low,close,volume',
#                 'token': api_key
#             }
#
#             data = requests.get(api_url, headers=headers, params=params)
#             data = data.json()
#
#         case '4hour'|'4h':
#
#             api_url = f"https://api.tiingo.com/iex/{ticker}/prices"
#             start_date = end_date-timedelta(hours=4000)
#             start_date = start_date.strftime('%Y-%m-%d')
#
#             params = {
#                 'startDate': start_date, # start_date,
#                 'endDate': end_date, # end_date,
#                 'resampleFreq': '4hour',
#                 'columns': 'open,high,low,close,volume',
#                 'token': api_key
#             }
#
#             data = requests.get(api_url, headers=headers, params=params)
#             data = data.json()
#
#         case 'minute'|'1min'|'min'|'1m'|'m':
#
#             api_url = f"https://api.tiingo.com/iex/{ticker}/prices"
#             start_date = end_date-timedelta(hours=100)
#             start_date = start_date.strftime('%Y-%m-%d')
#
#             params = {
#                 'startDate': start_date, # start_date,
#                 'endDate': end_date, # end_date,
#                 'resampleFreq': '1min',
#                 'columns': 'open,high,low,close,volume',
#                 'token': api_key
#             }
#
#             data = requests.get(api_url, headers=headers, params=params)
#             data = data.json()
#
#         case '5minutes'|'5min'|'5m':
#
#             api_url = f"https://api.tiingo.com/iex/{ticker}/prices"
#             start_date = end_date-timedelta(hours=1000)
#             start_date = start_date.strftime('%Y-%m-%d')
#
#             params = {
#                 'startDate': start_date, # start_date,
#                 'endDate': end_date, # end_date,
#                 'resampleFreq': '5min',
#                 'columns': 'open,high,low,close,volume',
#                 'token': api_key
#             }
#
#             data = requests.get(api_url, headers=headers, params=params)
#             data = data.json()
#
#         case '15minutes'|'15min'|'15m':
#
#             api_url = f"https://api.tiingo.com/iex/{ticker}/prices"
#             start_date = end_date-timedelta(hours=1000)
#             start_date = start_date.strftime('%Y-%m-%d')
#
#             params = {
#                 'startDate': start_date, # start_date,
#                 'endDate': end_date, # end_date,
#                 'resampleFreq': '15min',
#                 'columns': 'open,high,low,close,volume',
#                 'token': api_key
#             }
#
#             data = requests.get(api_url, headers=headers, params=params)
#             data = data.json()
#
#     df = create_df(data, time_period)
#
#     return df





from datetime import datetime, timedelta
import requests
from tiingo import TiingoClient
from src.data.fetch_data.utils.create_df import create_df

def fetch_data(time_period='daily', ticker='BTCUSD', start_date=None, end_date=None, api_key='Tiingo-API-Key'):
    """
    Fetch historical price data for a given ticker and time period.

    Parameters:
        time_period (str): Time period for the data (e.g., 'daily', 'hourly', '1min').
        ticker (str): Ticker symbol (e.g., 'BTCUSD').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        api_key (str): Tiingo API key.

    Returns:
        pd.DataFrame: DataFrame containing the fetched data.
    """
    # Set default end_date to today if not provided
    if end_date is None:
        end_date = datetime.now().date()

    # Initialize Tiingo client
    client = TiingoClient({'api_key': api_key, 'session': True})
    headers = {'Content-Type': 'application/json'}

    # Define time period configurations
    time_period_config = {
        'daily': {'frequency': 'daily', 'timedelta': None},
        '1day': {'frequency': 'daily', 'timedelta': None},
        'd': {'frequency': 'daily', 'timedelta': None},
        'weekly': {'frequency': 'weekly', 'timedelta': None},
        '1week': {'frequency': 'weekly', 'timedelta': None},
        'w': {'frequency': 'weekly', 'timedelta': None},
        'hourly': {'resampleFreq': '1hour', 'timedelta': timedelta(hours=2000)},
        '1hour': {'resampleFreq': '1hour', 'timedelta': timedelta(hours=2000)},
        'h': {'resampleFreq': '1hour', 'timedelta': timedelta(hours=2000)},
        '4hour': {'resampleFreq': '4hour', 'timedelta': timedelta(hours=4000)},
        '4h': {'resampleFreq': '4hour', 'timedelta': timedelta(hours=4000)},
        'minute': {'resampleFreq': '1min', 'timedelta': timedelta(hours=100)},
        '1min': {'resampleFreq': '1min', 'timedelta': timedelta(hours=100)},
        'min': {'resampleFreq': '1min', 'timedelta': timedelta(hours=100)},
        '1m': {'resampleFreq': '1min', 'timedelta': timedelta(hours=100)},
        'm': {'resampleFreq': '1min', 'timedelta': timedelta(hours=100)},
        '5minutes': {'resampleFreq': '5min', 'timedelta': timedelta(hours=1000)},
        '5min': {'resampleFreq': '5min', 'timedelta': timedelta(hours=1000)},
        '5m': {'resampleFreq': '5min', 'timedelta': timedelta(hours=1000)},
        '15minutes': {'resampleFreq': '15min', 'timedelta': timedelta(hours=1000)},
        '15min': {'resampleFreq': '15min', 'timedelta': timedelta(hours=1000)},
        '15m': {'resampleFreq': '15min', 'timedelta': timedelta(hours=1000)},
    }

    # Get the configuration for the specified time period
    config = time_period_config.get(time_period.lower())
    if not config:
        raise ValueError(f"Unsupported time period: {time_period}")

    # Calculate start_date if not provided
    if start_date is None and config['timedelta']:
        start_date = (datetime.now() - config['timedelta']).strftime('%Y-%m-%d')
    elif start_date is None:
        start_date = '2024-01-01'  # Default start date

    # Fetch data
    if 'frequency' in config:
        # Use TiingoClient for daily/weekly data
        data = client.get_ticker_price(ticker, startDate=start_date, endDate=end_date, frequency=config['frequency'])
    else:
        # Use requests.get() for intraday data
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

    # Create and return DataFrame
    df = create_df(data, time_period)
    return df
