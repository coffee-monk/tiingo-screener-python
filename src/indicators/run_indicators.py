import os
import pandas as pd
from pathlib import Path
from datetime import datetime
from src.indicators.get_indicators import get_indicators
from config.settings import TICKERS_DIR, INDICATORS_DIR

def run_indicators(indicator_list, params=None, timeframe_filter=None):
    """
    Process and save each ticker immediately after calculation.
    
    Args:
        indicator_list: List of indicators to calculate
        params: Dictionary of parameters for the indicators
        timeframe_filter: Optional timeframe to process (e.g., '1hour', 'daily')
                         If None, processes all timeframes
    """

    tickers_data = load_tickers(TICKERS_DIR)
    
    # Filter by timeframe if specified
    if timeframe_filter is not None:
        timeframe_filter = timeframe_filter.lower()
        tickers_data = {k: v for k, v in tickers_data.items() 
                       if v["timeframe"].lower() == timeframe_filter}
        if not tickers_data:
            print(f"\nNo files found for timeframe: {timeframe_filter}")
            return

    total_files = len(tickers_data)
    print('\n=== INDICATORS ===\n')
    print(f"Input directory: {TICKERS_DIR}")
    print(f"Output directory: {INDICATORS_DIR}")
    print(f"\nLoaded {total_files} datasets. Processing...")

    processed_count = 0
    for key, data in tickers_data.items():
        processed_count += 1
        ticker = data["ticker"]
        timeframe = data["timeframe"]
        
        print(f"\rProcessing {processed_count}/{total_files}: {str(ticker).strip().ljust(6)}", end="")       

        try:
            df_with_indicators = get_indicators(data["df"], indicator_list, params)
            
            save_ticker(
                df=df_with_indicators,
                ticker=ticker,
                timeframe=timeframe,
                date_stamp=data["date_stamp"],
                output_dir=INDICATORS_DIR
            )

        except KeyError as e:
            print(f"\nError processing {ticker}_{timeframe}: {str(e)}")
            continue
    
    print(f"\n\nAll files processed\n")

# Helper Functions ------------------------------------------------------------

def load_tickers(input_dir):
    """Load CSVs with datetime index and metadata."""
    tickers_data = {}
    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            parts = file.split("_")
            ticker, timeframe = parts[0], parts[1]
            date_stamp = parts[2].replace(".csv", "")
            
            df = pd.read_csv(
                os.path.join(input_dir, file),
                parse_dates=["date"],
                index_col="date"
            )
            df.attrs = {"timeframe": timeframe}
            
            tickers_data[f"{ticker}_{timeframe}"] = {
                "df": df,
                "ticker": ticker,
                "timeframe": timeframe,
                "date_stamp": date_stamp
            }
    return tickers_data


def save_ticker(df, ticker, timeframe, date_stamp, output_dir):
    """Save one processed ticker immediately."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{ticker}_{timeframe}_{date_stamp}.csv"
    filepath = os.path.join(output_dir, filename)
    
    df.to_csv(filepath, index=True, index_label="date")
