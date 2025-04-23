from src.visualization.src.subcharts.indicators import _add_visualizations
from src.visualization.src.subcharts.charts import ( _get_charts,
                                                     _prepare_dataframe, 
                                                     _configure_base_chart, 
                                                     _add_ui_elements )

def subcharts(df_list, ticker='', show_volume=False):
    """
    Visualize 4 different DataFrames with automatic interval detection.
    Now includes both Upper and Lower Supertrend bands, SMA, peaks/valleys/gap columns.
    """

    main_chart, charts = _get_charts(df_list)

    for i, (df, subchart) in enumerate(zip(df_list, charts)):

        df, interval = _prepare_dataframe(df, show_volume)

        _configure_base_chart(df, subchart)

        _add_ui_elements(subchart, charts, ticker, interval)

        _add_visualizations(subchart, df)

        subchart.set(df)

    main_chart.show(block=True)
