import os
import pandas as pd
from pathlib import Path
from src.fetch_data.fetch_ticker import fetch_ticker
from config.settings import TICKERS_DIR, TICKERS_LIST, DATE_STAMP

def fetch_tickers(
                  timeframes=['weekly', 'daily', 'hourly', '5min'], 
                  start_date=None,
                  end_date=None,
                  api_key='Tiingo_API_Key'
                 ):

    """Fetch raw ticker data for given timeframes without indicators."""

    print('\n=== FETCH TICKERS ===\n')
    print(f"Today's Date: {DATE_STAMP} (Format: DDMMYY)")
    print(f"Input Tickers: {TICKERS_LIST}")
    print(f"Output directory: {TICKERS_DIR}")
    
    # Load ticker list
    df_stock_list = load_tickers(TICKERS_LIST)
    total_tickers = len(df_stock_list['Ticker'].unique())
    print(f"\nLoaded {total_tickers} Tickers: {DATE_STAMP}")
    
    # Process each ticker
    processed_count = 0
    for ticker in df_stock_list['Ticker'].unique():
        processed_count += 1
        print(f"\rFetching {processed_count}/{total_tickers}: {str(ticker).strip().ljust(6)}", end="")
        process_ticker(ticker, timeframes, api_key)
    
    print("\n\nData fetch complete!")
    print(f"Raw data saved with date format: {DATE_STAMP}")
    print(f"Files formatted as: TICKER_TIMEFRAME_{DATE_STAMP}.csv")

# Ticker Handling -------------------------------------------------------------

def process_ticker(ticker, timeframes, api_key, save_to_disk=True):
    """Fetch and save raw ticker data for all specified timeframes."""
    results = {}
    
    for timeframe in timeframes:
        try:
            # Fetch raw data (no indicators applied)
            df = fetch_ticker(timeframe, ticker, api_key=api_key)
            results[timeframe] = df
            
            if save_to_disk:
                os.makedirs(TICKERS_DIR, exist_ok=True)
                filename = os.path.join(TICKERS_DIR, f"{ticker}_{timeframe}_{DATE_STAMP}.csv")
                df.to_csv(filename, index=True)
                
        except Exception as e:
            print(f"\nError fetching {ticker} ({timeframe}): {str(e)}")
            continue
            
    return results

def load_tickers(csv_path):

    df = pd.read_csv(csv_path)

    # Clean data - convert numeric columns and handle missing values
    numeric_cols = ['Last Sale', 'Net Change', '% Change', 'Market Cap', 'Volume']
    for col in numeric_cols:
        try: df[col] = df[col].replace('[\$,%]', '', regex=True).astype(float)
        except Exception as e:
            # print(f"\nError fetching csv: {str(e)}")
            continue

    return df
