import os
import pandas as pd
from pathlib import Path
from datetime import datetime
from src.indicators.get_indicators import get_indicators

PROJECT_ROOT = Path(__file__).parent.parent.parent
INPUT_DIR = PROJECT_ROOT / "data/tickers"
OUTPUT_DIR = PROJECT_ROOT / "data/indicators"

def run_indicators(indicator_list, params=None):
    """Process and save each ticker immediately after calculation."""

    ticker_data = load_ticker(INPUT_DIR)
    total_files = len(ticker_data)
    print(f"Loaded {total_files} datasets. Processing...")

    processed_count = 0
    for key, data in ticker_data.items():
        processed_count += 1
        ticker = data["ticker"]
        timeframe = data["timeframe"]
        
        print(f"\rProcessing {processed_count}/{total_files}: {ticker.ljust(6)}", end="")       

        df_with_indicators = get_indicators(data["df"], indicator_list, params)
        
        save_ticker(
            df=df_with_indicators,
            ticker=ticker,
            timeframe=timeframe,
            date_stamp=data["date_stamp"],
            output_dir=OUTPUT_DIR
        )
    
    print(f"\nAll files processed. Results saved to: {OUTPUT_DIR}")

# Helper Functions ------------------------------------------------------------

def load_ticker(input_dir):
    """Load CSVs with datetime index and metadata."""
    ticker_data = {}
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
            df.attrs = {"time_period": timeframe}
            
            ticker_data[f"{ticker}_{timeframe}"] = {
                "df": df,
                "ticker": ticker,
                "timeframe": timeframe,
                "date_stamp": date_stamp
            }
    return ticker_data


def save_ticker(df, ticker, timeframe, date_stamp, output_dir):
    """Save one processed ticker immediately."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{ticker}_{timeframe}_indicators_{date_stamp}.csv"
    filepath = os.path.join(output_dir, filename)
    
    # Save with index (datetime) as a column
    df.to_csv(filepath, index=True, index_label="date")  
