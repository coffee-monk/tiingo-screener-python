import pandas as pd
import numpy as np
from src.indicators.peaks_valleys import calculate_peaks_valleys
from src.indicators.gaps import calculate_gaps

def calculate_peaks_valleys_aVWAP(df, anchor_column, anchor_values):
    """
    Calculate aVWAPs anchored at peaks or valleys.

    Parameters:
        df (pd.DataFrame): The DataFrame containing price and volume data.
        anchor_column (str): The name of the anchor column (e.g., 'Valleys' or 'Peaks').
        anchor_values (pd.Series): The values of the anchor column (e.g., peaks or valleys).

    Returns:
        dict: A dictionary of aVWAPs anchored at peaks or valleys.
    """
    df['hlc3'] = (df['High'] + df['Low'] + df['Close']) / 3

    aVWAPs = {}  # Dictionary to store full aVWAPs
    for i in range(len(df)):
        if anchor_values.iloc[i] == 1.0:  # Check for anchor point
            # Initialize cumulative values
            cumulative_price_volume = 0.0
            cumulative_volume = 0.0
            # Calculate aVWAP from this point to the end
            aVWAP = []
            for j in range(i, len(df)):
                cumulative_price_volume += df['hlc3'].iloc[j] * df['Volume'].iloc[j]
                cumulative_volume += df['Volume'].iloc[j]
                if cumulative_volume > 0:
                    aVWAP.append(cumulative_price_volume / cumulative_volume)
                else:
                    aVWAP.append(np.nan)
            # Pad the beginning with NaN (before the anchor point)
            aVWAP = [np.nan] * i + aVWAP
            # Store the aVWAP in the dictionary
            aVWAPs[f'{anchor_column}_aVWAP_{i+1}'] = aVWAP

    return aVWAPs

def calculate_gaps_aVWAP(df, gap_up_values, gap_down_values):
    """
    Calculate aVWAPs anchored at gaps (Gap_Up or Gap_Down).

    Parameters:
        df (pd.DataFrame): The DataFrame containing price and volume data.
        gap_up_values (pd.Series): The values of the 'Gap_Up' column.
        gap_down_values (pd.Series): The values of the 'Gap_Down' column.

    Returns:
        dict: A dictionary of aVWAPs anchored at gaps.
    """
    df['hlc3'] = (df['High'] + df['Low'] + df['Close']) / 3

    gap_aVWAPs = {}  # Dictionary to store gap aVWAPs
    for i in range(len(df)):
        if gap_up_values.iloc[i] == 1 or gap_down_values.iloc[i] == 1:  # Check for gap
            # Initialize cumulative values
            cumulative_price_volume = 0.0
            cumulative_volume = 0.0
            # Calculate aVWAP from this point to the end
            aVWAP = []
            for j in range(i, len(df)):
                cumulative_price_volume += df['hlc3'].iloc[j] * df['Volume'].iloc[j]
                cumulative_volume += df['Volume'].iloc[j]
                if cumulative_volume > 0:
                    aVWAP.append(cumulative_price_volume / cumulative_volume)
                else:
                    aVWAP.append(np.nan)
            # Pad the beginning with NaN (before the gap point)
            aVWAP = [np.nan] * i + aVWAP
            # Store the aVWAP in the dictionary
            gap_type = 'Gap_Up' if gap_up_values.iloc[i] == 1 else 'Gap_Down'
            gap_aVWAPs[f'{gap_type}_aVWAP_{i+1}'] = aVWAP

    return gap_aVWAPs

def calculate_indicator(df):
    """
    Calculate peaks, valleys, and gap aVWAPs.

    Parameters:
        df (pd.DataFrame): The DataFrame containing price, volume, and gap data.

    Returns:
        pd.DataFrame: A DataFrame containing peaks, valleys, gaps, and aVWAPs.
    """
    # Calculate peaks, valleys, and gaps
    peaks_valleys = calculate_peaks_valleys(df)
    gaps = calculate_gaps(df)

    # Extract the values for peaks, valleys, and gaps
    valleys_values = peaks_valleys['Valleys']
    peaks_values = peaks_valleys['Peaks']
    gap_up_values = gaps['Gap_Up']
    gap_down_values = gaps['Gap_Down']

    # Calculate aVWAPs for peaks, valleys, and gaps
    valley_aVWAPs = calculate_peaks_valleys_aVWAP(df, 'Valleys', valleys_values)
    peak_aVWAPs = calculate_peaks_valleys_aVWAP(df, 'Peaks', peaks_values)
    gap_aVWAPs = calculate_gaps_aVWAP(df, gap_up_values, gap_down_values)

    # Create a dictionary to store all results
    results = {
        'Valleys': valleys_values,
        'Peaks': peaks_values,
        'Gap_Up': gap_up_values,
        'Gap_Down': gap_down_values,
        **valley_aVWAPs,  # Add valley aVWAPs
        **peak_aVWAPs,    # Add peak aVWAPs
        **gap_aVWAPs      # Add gap aVWAPs
    }

    # Convert the results dictionary to a DataFrame
    results_df = pd.DataFrame(results)

    # Print the first 10 rows for debugging
    print(results_df.head(10))

    # Return the results as a DataFrame
    return results_df
