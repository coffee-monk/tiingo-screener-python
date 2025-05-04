import os
import pandas as pd
from pathlib import Path
from datetime import datetime
from src.fetch_data.fetch_ticker import fetch_ticker

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATE_STAMP = datetime.now().strftime("%d%m%y")
OUTPUT_DIR = PROJECT_ROOT / "data/tickers"

print(f"Output directory: {OUTPUT_DIR}")
print(f"Using date format: {DATE_STAMP}")

def fetch_tickers(
                 TIMEFRAMES=['day'], 
                 start_date=None,
                 end_date=None,
                 API_KEY='Tiingo_API_Key'
                 ):

    """Fetch raw ticker data for given timeframes without indicators."""
    
    # Load ticker list
    df_stock_list = load_tickers()
    total_tickers = len(df_stock_list['Ticker'].unique())
    print(f"\nLoaded {total_tickers} tickers | Date: {DATE_STAMP}")
    
    # Process each ticker
    processed_count = 0
    for ticker in df_stock_list['Ticker'].unique():
        processed_count += 1
        print(f"\rFetching {processed_count}/{total_tickers}: {ticker.ljust(6)}", end="")
        process_ticker(ticker, TIMEFRAMES, API_KEY)
    
    print("\n\nData fetch complete!")
    print(f"Raw data saved with date format: {DATE_STAMP}")
    print(f"Files formatted as: TICKER_TIMEFRAME_{DATE_STAMP}.csv")

# Ticker Handling -----------------------------------------------------------==

def process_ticker(ticker, TIMEFRAMES, API_KEY, save_to_disk=True):
    """Fetch and save raw ticker data for all specified timeframes."""
    results = {}
    
    for timeframe in TIMEFRAMES:
        try:
            # Fetch raw data (no indicators applied)
            df = fetch_ticker(timeframe, ticker, api_key=API_KEY)
            results[timeframe] = df
            
            if save_to_disk:
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                filename = os.path.join(OUTPUT_DIR, f"{ticker}_{timeframe}_{DATE_STAMP}.csv")
                df.to_csv(filename, index=True)
                
        except Exception as e:
            print(f"\nError fetching {ticker} ({timeframe}): {str(e)}")
            continue
            
    return results

def load_tickers():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    csv_path = os.path.join(project_root, 'fetch_data', 'ticker_lists', 'nasdaq_tickers.csv')

    print(csv_path)

    df = pd.read_csv(csv_path)

    # Clean data - convert numeric columns, handle missing values
    numeric_cols = ['Last Sale', 'Net Change', '% Change', 'Market Cap', 'Volume']
    for col in numeric_cols:
        df[col] = df[col].replace('[\$,%]', '', regex=True).astype(float)

    return df
