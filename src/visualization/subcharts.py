from src.visualization.src.subcharts.indicators import add_visualizations
from src.visualization.src.subcharts.charts import (
    get_charts,
    prepare_dataframe, 
    configure_base_chart, 
    add_ui_elements
)

TIMEFRAME_ORDER = [ 'weekly', 'week', 'daily', 'day', '4hour', 'hourly', '1hour', '15min', '5min', '1min' ]

def subcharts(df_list, ticker='', show_volume=False):
    """
    Visualize 1-4 DataFrames with automatic timeframe ordering.
    DataFrames are now sorted from largest to smallest timeframe (weekly → daily → 15min etc).
    """
    # Sort DataFrames by timeframe priority
    df_list = sorted(
        df_list,
        key=lambda x: (
            TIMEFRAME_ORDER.index(x.attrs['timeframe']) 
            if x.attrs.get('timeframe') in TIMEFRAME_ORDER 
            else float('inf')  # Unknown timeframes go last
        )
    )

    main_chart, subcharts = get_charts(df_list)

    for i, (df, subchart) in enumerate(zip(df_list, subcharts)):
        df, interval = prepare_dataframe(df, show_volume)
        configure_base_chart(df, subchart)
        add_ui_elements(subchart, subcharts, ticker, interval)
        add_visualizations(subchart, df)
        subchart.set(df)

    main_chart.show(block=True)
