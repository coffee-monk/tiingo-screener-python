import pandas as pd
from src.indicators.get_indicators import get_indicators
from src.visualization.src.color_palette import get_color_palette

def calculate_candle_colors(df, default_color='QQEMOD'):
    colors = get_color_palette()
    
    # Get indicators - now includes all QQEMOD outputs
    df = get_indicators(df, ['zscore', 'RSI', 'QQEMOD'])
    
    def map_zscore(zscore):
        if zscore <= -3.0:          return colors['red_dark']
        elif -3.0 < zscore <= -2.5: return colors['red_dark']
        elif -2.5 < zscore <= -2.0: return colors['red_dark']
        elif -2.0 < zscore <= -1.5: return colors['red']
        elif -1.5 < zscore <= -1.0: return colors['red_trans_3']
        elif -1.0 < zscore <= -0.5: return colors['red_trans_2']
        elif -0.5 < zscore <= 0:    return colors['red_trans_1'] 
        elif 0 < zscore <= 0.5:     return colors['teal_trans_1'] 
        elif 0.5 < zscore <= 1.0:   return colors['teal_trans_2']
        elif 1.0 < zscore <= 1.5:   return colors['teal_trans_3']
        elif 1.5 < zscore <= 2.0:   return colors['teal']
        elif 2.0 < zscore <= 2.5:   return colors['aqua']
        elif 2.5 < zscore <= 3.0:   return colors['aqua']
        else:                       return colors['aqua']

    def map_RSI(RSI):
        if 0 < RSI <= 30:    return colors['red_dark']
        elif 30 < RSI <= 35: return colors['red_trans_3']
        elif 35 < RSI <= 40: return colors['red_trans_2']
        elif 40 < RSI <= 45: return colors['red_trans_1']
        elif 45 < RSI <= 50: return colors['red_trans_0']
        elif 50 < RSI <= 55: return colors['teal_trans_0']
        elif 55 < RSI <= 60: return colors['teal_trans_1']
        elif 60 < RSI <= 65: return colors['teal_trans_2']
        elif 65 < RSI <= 70: return colors['teal_trans_3']
        elif 70 < RSI <= 100: return colors['aqua']
        else:                return colors['black']

    def map_QQEMOD(QQEMOD):
        if QQEMOD['QQE1_Above_Upper'] and QQEMOD['QQE2_Above_Threshold']:
            return colors['teal'] if QQEMOD['QQE2_Above_TL'] else colors['teal_trans_3']
        elif QQEMOD['QQE1_Below_Lower'] and QQEMOD['QQE2_Below_Threshold']:
            return colors['red'] if not QQEMOD['QQE2_Above_TL'] else colors['red_trans_3']

        elif QQEMOD['QQE2_Above_Threshold']: return colors['teal_trans_1']  
        elif QQEMOD['QQE2_Below_Threshold']: return colors['red_trans_1']  
        else: return colors['black'] 

    # Apply mappings
    df['RSI_color']    = df['RSI'].apply(map_RSI)
    df['ZScore_color'] = df['ZScore'].apply(map_zscore)
    df['QQEMOD_color'] = df.apply(map_QQEMOD, axis=1)
    
    return {
        'color': df[f"{default_color}_color"],
        'RSI_color': df['RSI_color'],
        'ZScore_color': df['ZScore_color'],
        'QQEMOD_color': df['QQEMOD_color']
    }

def calculate_indicator(df, **params):
    return calculate_candle_colors(df, **params)
