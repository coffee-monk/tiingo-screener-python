import pandas as pd
from collections import Counter

def detect_interval(df):
    """
    Automatically detect the most common time interval between data points.
    Returns a string like '1min', '5min', '1hour', '4hour', 'daily', etc.
    """
    if 'date' not in df.columns:
        return 'unknown'
   
    # Calculate time differences between consecutive rows
    time_diffs = pd.Series(pd.to_datetime(df['date'])).diff().dropna()
   
    # Convert to minutes
    diffs_minutes = time_diffs.dt.total_seconds() / 60
   
    # Round to nearest standard interval
    rounded_diffs = diffs_minutes.round(0)
   
    # Count occurrences of each interval
    diff_counts = Counter(rounded_diffs)
   
    # Get the most common interval in minutes
    most_common_min = diff_counts.most_common(1)[0][0]
   
    # Map to standard interval names
    interval_map = {
        1: '1min',
        5: '5min',
        15: '15min',
        30: '30min',
        60: '1hour',
        240: '4hour',
        1440: 'daily',
        10080: 'weekly'
    }
   
    # Find the closest standard interval
    closest_interval = min(interval_map.keys(), key=lambda x: abs(x - most_common_min))
    return interval_map.get(closest_interval, f'{int(most_common_min)}min')
