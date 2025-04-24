from src.visualization.src.subcharts.indicators import add_visualizations
from src.visualization.src.subcharts.charts import ( get_charts,
                                                     prepare_dataframe, 
                                                     configure_base_chart, 
                                                     add_ui_elements )


def subcharts(df_list, ticker='', show_volume=False):
    """
    Visualize 1-4 different DataFrames with automatic interval detection.
    Now includes both Upper and Lower Supertrend bands, SMA, peaks/valleys/gap columns.
    """

    main_chart, subcharts = get_charts(df_list)

    for i, (df, subchart) in enumerate(zip(df_list, subcharts)):

        df, interval = prepare_dataframe(df, show_volume)

        configure_base_chart(df, subchart)

        add_ui_elements(subchart, subcharts, ticker, interval)

        add_visualizations(subchart, df)

        subchart.set(df)

    main_chart.show(block=True)
