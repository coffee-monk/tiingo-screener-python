# Custom Inputs for run_scanner() =========================

# CRITERIA PER TIMEFRAME ================================== 

# daily + 1hour ------------------------------------------- 
 
dh_OBBullish_support = { 
                        'daily': ['OB_bullish_below_aVWAP'],
                        '1hour': ['OB_bullish_support']
                       }

dh_OBBearish_resistance = { 
                           'daily': ['OB_bearish_above_aVWAP'],
                           '1hour': ['OB_bearish_resistance']
                          }

dh_OBBearish_resistance = { 
                           'daily': ['OB_bearish_above_aVWAP'],
                           '1hour': ['OB_bearish_resistance']
                          }

dh_divergences_bullish = { 
                          'daily': ['divergences_bullish'],
                          '1hour': ['divergences_bullish']
                         }

dh_divergences_bearish = { 
                          'daily': ['divergences_bearish'],
                          '1hour': ['divergences_bearish']
                         }

dh_StDev_oversold_OBBullish = { 
                               'daily': ['StDev_oversold'],
                               '1hour': ['OB_bullish_below_aVWAP']
                              }

dh_StDev_overbought_OBBearish = { 
                                 'daily': ['StDev_overbought'],
                                 '1hour': ['OB_bearish_above_aVWAP']
                                }
