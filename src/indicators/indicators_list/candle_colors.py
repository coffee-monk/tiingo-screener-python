import pandas as pd
from src.indicators.get_indicators import get_indicators
from src.visualization.src.color_palette import get_color_palette

def calculate_candle_colors(df, indicator_color='ZScore'):

    # Indicator Color Options: 'ZScore', 'RSI', 'QQEMOD', 'banker_RSI', 'WAE', 'supertrend'

    df = get_indicators(df, [indicator_color.split('_')[0]])

    colors = get_color_palette()

    # Define color mapping functions
    def map_zscore(zscore):
        if          zscore <= -3.0: return colors['magenta']
        elif -3.0 < zscore <= -2.5: return colors['red_dark']
        elif -2.5 < zscore <= -2.0: return colors['red']
        elif -2.0 < zscore <= -1.5: return colors['red']
        elif -1.5 < zscore <= -1.0: return colors['red_trans_3']
        elif -1.0 < zscore <= -0.5: return colors['red_trans_2']
        elif -0.5 < zscore <=    0: return colors['red_trans_1'] 
        elif    0 < zscore <=  0.5: return colors['teal_trans_1'] 
        elif  0.5 < zscore <=  1.0: return colors['teal_trans_2']
        elif  1.0 < zscore <=  1.5: return colors['teal_trans_3']
        elif  1.5 < zscore <=  2.0: return colors['teal_trans_3']
        elif  2.0 < zscore <=  2.5: return colors['teal']
        elif  2.5 < zscore <=  3.0: return colors['teal']
        elif  3.0 < zscore:         return colors['neon']
        return colors['black']

    def map_banker_RSI(banker_RSI):
        if    15 <= banker_RSI <=   20: return colors['neon']
        elif  11 <= banker_RSI <= 14.9: return colors['aqua']
        elif 5.1 <= banker_RSI <=   10: return colors['teal']
        elif 0.1 <= banker_RSI <=    5: return colors['teal_trans_3']
        return colors['black']

    def map_RSI(RSI):
        if    0 < RSI <=  30: return colors['red_dark']
        elif 30 < RSI <=  35: return colors['red_trans_3']
        elif 35 < RSI <=  40: return colors['red_trans_2']
        elif 40 < RSI <=  45: return colors['red_trans_1']
        elif 45 < RSI <=  50: return colors['red_trans_0']
        elif 50 < RSI <=  55: return colors['teal_trans_0']
        elif 55 < RSI <=  60: return colors['teal_trans_1']
        elif 60 < RSI <=  65: return colors['teal_trans_2']
        elif 65 < RSI <=  70: return colors['teal_trans_3']
        elif 70 < RSI <= 100: return colors['aqua']
        return colors['black']

    def map_QQEMOD(row):
        if row['QQE1_Above_Upper'] and row['QQE2_Above_Threshold']:
            return colors['teal'] if row['QQE2_Above_TL'] else colors['teal_trans_3']
        elif row['QQE1_Below_Lower'] and row['QQE2_Below_Threshold']:
            return colors['red'] if not row['QQE2_Above_TL'] else colors['red_trans_3']
        elif row['QQE2_Above_Threshold']: return colors['teal_trans_1']  
        elif row['QQE2_Below_Threshold']: return colors['red_trans_1']  
        return colors['black']

    def map_WAE(row):
        direction = row['WAE_Direction']
        momentum = row['WAE_Momentum']
        is_exploding = row['WAE_Upper'] > df['WAE_Upper'].mean()
        if direction < 0:
            if   momentum > 3.0: return colors['red_dark'] if is_exploding else colors['red']
            elif momentum > 2.0: return colors['red_dark'] if is_exploding else colors['red_trans_3']
            elif momentum > 1.0: return colors['red_dark'] if is_exploding else colors['red_trans_3']
            elif momentum > 0.5: return colors['red_trans_2']
        else:
            if   momentum > 3.0: return colors['aqua'] if is_exploding else colors['teal']
            elif momentum > 2.0: return colors['aqua'] if is_exploding else colors['teal_trans_3']
            elif momentum > 1.0: return colors['aqua'] if is_exploding else colors['teal_trans_3']
            elif momentum > 0.5: return colors['teal_trans_2']
        return colors['black']

    def map_supertrend(row):
        return colors['teal'] if row['Supertrend_Direction'] > 0 else colors['red']

    # Create a mapping of indicator to their color functions
    color_mappers = {
        'ZScore': lambda df: df['ZScore'].apply(map_zscore),
        'RSI': lambda df: df['RSI'].apply(map_RSI),
        'banker_RSI': lambda df: df['banker_RSI'].apply(map_banker_RSI),
        'QQEMOD': lambda df: df.apply(map_QQEMOD, axis=1),
        'WAE': lambda df: df.apply(map_WAE, axis=1),
        'supertrend': lambda df: df.apply(map_supertrend, axis=1),
    }

    # Get the base indicator name (before _color)
    base_indicator = indicator_color.split('_color')[0] if '_color' in indicator_color else indicator_color
    
    # Apply only the needed color mapping
    if base_indicator in color_mappers:
        color_series = color_mappers[base_indicator](df)
        return {'color': color_series}
    
    return {'color': pd.Series([colors['black']] * len(df), index=df.index)}


def calculate_indicator(df, **params):
    return calculate_candle_colors(df, **params)
