import requests
from tiingo import TiingoClient
from src.data.fetch_data.utils.create_df import create_df
from datetime import datetime, timedelta

def fetch_data(time_period='daily', 
               ticker='BTCUSD', 
               start_date='2024-01-01', 
               end_date=datetime.now().date(), 
               api_key='Tiingo-API-Key'):

    client = TiingoClient({'api_key': api_key, 'session': True})
    headers = {'Content-Type': 'application/json'}

    # Map time_period to Tiingo frequency
    frequency_map = {
        'daily': 'daily',
        '1day': 'daily',
        'd': 'daily',
        'weekly': 'weekly',
        '1week': 'weekly',
        'w': 'weekly',
        'hourly': '1hour',
        '1hour': '1hour',
        'h': '1hour'
    }
    frequency = frequency_map.get(time_period, 'daily')  # Default to 'daily'

    # Define the order of asset types to try
    asset_types = ['forex', 'crypto', 'stock']

    # Try fetching data for each asset type in sequence
    for asset_type in asset_types:
        try:
            match asset_type:
                # case 'forex':
                #     if frequency == '1hour':
                #         print('forex test')
                #         # Use the forex endpoint for hourly forex data
                #         url = f"https://api.tiingo.com/tiingo/fx/{ticker}/prices"
                #         params = {
                #             'startDate': start_date,
                #             'endDate': end_date.strftime('%Y-%m-%d'),
                #             'resampleFreq': '1hour',
                #             'token': api_key
                #         }
                #         response = requests.get(url, headers=headers, params=params)
                #         data = response.json()

                # case 'crypto':
                #         print('crypto')
                #         print('')
                #         url = f"https://api.tiingo.com/tiingo/crypto/{ticker}/prices"
                #         print('crypto')
                #         params = {
                #             'startDate': start_date,
                #             'endDate': end_date.strftime('%Y-%m-%d'),
                #             'resampleFreq': '1hour',
                #             'token': api_key
                #         }
                #         print('crypto')
                #         response = requests.get(url, headers=headers, params=params)
                #         print(response)
                #         data = response.json()
                #         print('TEST')
                #         print('')
                #         print(data)

                case 'stock':
                    if frequency == '1hour':
                        print('stock test')
                        # Use the IEX endpoint for hourly stock, ETF, and index data
                        url = f"https://api.tiingo.com/iex/{ticker}/prices"
                        params = {
                            'startDate': (end_date - timedelta(days=200)).strftime('%Y-%m-%d'),
                            'endDate': end_date.strftime('%Y-%m-%d'),
                            'resampleFreq': '1hour',
                            'columns': 'open,high,low,close,volume',
                            'token': api_key
                        }
                        response = requests.get(url, headers=headers, params=params)
                        data = response.json()
                        print(data)
                    else:
                        # Use the daily/weekly endpoint for stocks, ETFs, and indices
                        data = client.get_ticker_price(ticker, startDate=start_date, endDate=end_date, frequency=frequency)
                        print(data)

            # If data is successfully fetched, break out of the loop
            if data:
                break

        except Exception as e:
            # If an error occurs, try the next asset type
            print(f"Failed to fetch data as {asset_type}: {e}")
            continue

    else:
        # If no asset type succeeds, raise an error
        raise ValueError(f"Could not fetch data for ticker {ticker}. Please check the ticker symbol and try again.")

    # Convert data to DataFrame
    # print(data)
    df = create_df(data, time_period)

    return df
