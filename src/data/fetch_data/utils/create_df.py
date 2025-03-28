from pprint import pprint
import pandas as pd
from datetime import datetime

def create_df(data, time_period='daily'):

    df = pd.DataFrame(data)

    match time_period:

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

    print(df.head(10))

    return df
