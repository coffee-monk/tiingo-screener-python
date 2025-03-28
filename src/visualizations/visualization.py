import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np

def calculate_aVWAP_avg(df):

    aVWAP_columns = [col for col in df.columns if col.startswith(('Valleys_aVWAP', 'Peaks_aVWAP', 'Gap_Up_aVWAP', 'Gap_Down_aVWAP'))]

    # Calculate the average aVWAP at each timestamp
    aVWAP_avg = df[aVWAP_columns].mean(axis=1)

    return aVWAP_avg

def visualization(df, visualization_name='None'):

    match visualization_name:
        case 'aVWAP_channel':
            addplots = []
            for col in df.columns:
                if col.startswith('Valleys_aVWAP'):
                    # Find the anchor point (first non-NaN value)
                    anchor_index = df[col].first_valid_index()
                    if anchor_index is not None:
                        # Get the volume at the anchor point
                        anchor_volume = df.loc[anchor_index, 'Volume']
                        # Scale alpha based on anchor volume
                        alpha_value = (anchor_volume / df['Volume'].max())  # Normalize to [0, 1]
                        addplots.append(mpf.make_addplot(df[col], color='orange', linestyle='solid', label=col, alpha=0.9))

                if col.startswith('Peaks_aVWAP'):
                    # Find the anchor point (first non-NaN value)
                    anchor_index = df[col].first_valid_index()
                    if anchor_index is not None:
                        # Get the volume at the anchor point
                        anchor_volume = df.loc[anchor_index, 'Volume']
                        # Scale alpha based on anchor volume
                        alpha_value = (anchor_volume / df['Volume'].max())  # Normalize to [0, 1]
                        addplots.append(mpf.make_addplot(df[col], color='orange', linestyle='solid', alpha=0.9))

            # Add gray aVWAP lines starting from gap candles (using existing aVWAP values)
            for col in df.columns:
                if col.startswith(('Gap_Up_aVWAP', 'Gap_Down_aVWAP')):
                    # Find the anchor point (first non-NaN value)
                    anchor_index = df[col].first_valid_index()
                    if anchor_index is not None:
                        # Get the volume at the anchor point
                        anchor_volume = df.loc[anchor_index, 'Volume']
                        # Scale alpha based on anchor volume
                        alpha_value = (anchor_volume / df['Volume'].max())  # Normalize to [0, 1]
                        addplots.append(mpf.make_addplot(df[col], color='gray', linestyle='solid', alpha=alpha_value, label=col))

            # Calculate and plot the average aVWAP (including peaks, valleys, and gaps)
            df['aVWAP_avg'] = calculate_aVWAP_avg(df)
            addplots.append(mpf.make_addplot(df['aVWAP_avg'], color='yellow', linestyle='solid', alpha=0.7, label='aVWAP_avg'))

            if addplots:  # Only plot if additional plots to add
                fig, _ = mpf.plot(
                    df,
                    type='line',
                    style='nightclouds',
                    addplot=addplots,
                    show_nontrading=False,
                    returnfig=True,
                    figsize=(14, 10),
                    # volume=True
                )
            else:
                fig, _ = mpf.plot(
                    df,
                    type='line',
                    # style='nightclouds',
                    style=s,
                    show_nontrading=False,
                    returnfig=True,
                    figsize=(14, 10),
                    # volume=True
                )

            for ax in fig.axes:
                ax.legend().remove()

            plt.show()

        case 'None':
            print(df.head(5))
