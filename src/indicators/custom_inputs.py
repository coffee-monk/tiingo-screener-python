# Custom Inputs for get_indicators() ======================

# PARAMETERS ----------------------------------------------

ind_configs = {

    # Indicator Lists by Timeframe ========================

    'indicators': {

        'weekly': [
            'aVWAP', 
            'candle_colors', 
            'StDev', 
            'QQEMOD', 
            'banker_RSI',
            'SMA',
            'supertrend', 
            'OB', 
            'TTM_squeeze', 
            'divergence_Vortex', 'divergence_Fisher', 'divergence_OBV', 'divergence_Volume'
        ],

        'daily': [
            'aVWAP', 
            'candle_colors', 
            'StDev', 
            'QQEMOD', 
            'banker_RSI',
            'SMA',
            'supertrend', 
            'OB', 
            'TTM_squeeze', 
            'divergence_Vortex', 'divergence_Fisher', 'divergence_OBV', 'divergence_Volume'
        ],

        '1hour': [
            'aVWAP', 
            'candle_colors', 
            'StDev', 
            'QQEMOD', 
            'banker_RSI',
            'SMA',
            'supertrend', 
            'OB', 
            'TTM_squeeze', 
            'divergence_Vortex', 'divergence_Fisher', 'divergence_OBV', 'divergence_Volume'
        ],

        '5min': [
            'aVWAP', 
            'candle_colors', 
            'liquidity', 
            'StDev', 
            'QQEMOD',
            'banker_RSI', 
            'SMA', 
            'supertrend', 
            'OB', 
            'TTM_squeeze',
            'divergence_Vortex', 'divergence_Fisher', 'divergence_OBV', 'divergence_Volume'
        ]
    },

    # Parameter Lists by Timeframe ========================

    'params': {

        # Weekly ------------------------------------------

        'weekly': {
            'candle_colors': {
                'indicator_color': 'StDev',
                'custom_params': {
                    'StDev': {
                        'std_lookback': 4, 'avg_lookback': 4,
                        'centreline': 'peaks_valleys_avg',
                        'peaks_valleys_params': {'periods': 8, 'max_aVWAPs': None}
                    }
                }
            },
            'aVWAP': {
                'peaks_valleys': False, 
                'peaks_valleys_avg': True,
                'peaks_valleys_params': {'periods': 8, 'max_aVWAPs': None},
                'OB': True, 
                'OB_avg': False,
                'OB_params': {'periods': 4, 'max_aVWAPs': None},
                'gaps': False, 
                'gaps_avg': False,
                'gaps_params': {'max_aVWAPs': 4},
                'avg_lookback': 8, 
                'keep_OB_column': True
            },
            'OB': {'periods': 4},
            'StDev': {
                'centreline': 'peaks_valleys_avg',
                'peaks_valleys_params': {'periods': 8, 'max_aVWAPs': None},
                'std_lookback': 4, 'avg_lookback': 4
            },
            'QQEMOD': {
                'rsi_period': 8, 'rsi_period2': 4, 'sf': 8, 'sf2': 4,
                'qqe_factor': 3.0, 'qqe_factor2': 1.61, 'threshold': 3,
                'bb_length': 8, 'bb_multi': 0.35
            },
            'SMA': {'periods': [50, 200]},
            'liquidity': {'swing_length': 4, 'range_percent': 0.1},
            'supertrend': {'period': 8, 'multiplier': 3},
            'TTM_squeeze': {
                'bb_length': 8, 'bb_std_dev': 2.0,
                'kc_length': 8, 'kc_mult': 1.5, 'use_true_range': True
            },
            'divergence_OBV': {'period': 26, 'lookback': 26},
            'divergence_Volume': {'period': 26, 'lookback': 26},
            'divergence_Fisher': {'period': 26, 'lookback': 26},
            'divergence_Vortex': {'period': 26, 'lookback': 26}
        },

        # Daily -------------------------------------------

        'daily': {
            'candle_colors': {
                'indicator_color': 'StDev',
                'custom_params': {
                    'StDev': {
                        'std_lookback': 20, 'avg_lookback': 20,
                        'centreline': 'peaks_valleys_avg',
                        'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None}
                    }
                }
            },
            'aVWAP': {
                'peaks_valleys': False, 
                'peaks_valleys_avg': False,
                'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None},
                'OB': True, 
                'OB_avg': False,
                'OB_params': {'periods': 20, 'max_aVWAPs': None},
                'gaps': False, 
                'gaps_avg': False,
                'gaps_params': {'max_aVWAPs': 20},
                'avg_lookback': 5, 
                'keep_OB_column': False
            },
            'OB': {'periods': 20},
            'StDev': {
                'centreline': 'peaks_valleys_avg',
                'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None},
                'std_lookback': 20, 'avg_lookback': 20
            },
            'QQEMOD': {
                'rsi_period': 10, 'rsi_period2': 5, 'sf': 10, 'sf2': 5,
                'qqe_factor': 3.0, 'qqe_factor2': 1.61, 'threshold': 3,
                'bb_length': 20, 'bb_multi': 0.35
            },
            'SMA': {'periods': [50, 200]},
            'liquidity': {'swing_length': 20, 'range_percent': 0.1},
            'supertrend': {'period': 20, 'multiplier': 3},
            'TTM_squeeze': {
                'bb_length': 40, 'bb_std_dev': 2.0,
                'kc_length': 40, 'kc_mult': 1.5, 'use_true_range': True
            },
            'divergence_OBV': {'period': 50, 'lookback': 50},
            'divergence_Volume': {'period': 50, 'lookback': 50},
            'divergence_Fisher': {'period': 50, 'lookback': 50},
            'divergence_Vortex': {'period': 50, 'lookback': 50}
        },

        # 1Hour -------------------------------------------

        '1hour': {
            'candle_colors': {
                'indicator_color': 'StDev',
                'custom_params': {
                    'StDev': {
                        'std_lookback': 16, 'avg_lookback': 16,
                        'centreline': 'peaks_valleys_avg',
                        'peaks_valleys_params': {'periods': 16, 'max_aVWAPs': None}
                    }
                }
            },
            'aVWAP': {
                'peaks_valleys': False, 
                'peaks_valleys_avg': False,
                'peaks_valleys_params': {'periods': 16, 'max_aVWAPs': None},
                'OB': True, 
                'OB_avg': False,
                'OB_params': {'periods': 16, 'max_aVWAPs': 5},
                'gaps': False, 
                'gaps_avg': False,
                'gaps_params': {'max_aVWAPs': 16},
                'avg_lookback': 16, 
                'keep_OB_column': True
            },
            'OB': {'periods': 16},
            'StDev': {
                'centreline': 'peaks_valleys_avg',
                'peaks_valleys_params': {'periods': 16, 'max_aVWAPs': None},
                'std_lookback': 16, 'avg_lookback': 16
            },
            'QQEMOD': {
                'rsi_period': 6, 'rsi_period2': 5, 'sf': 6, 'sf2': 5,
                'qqe_factor': 3.0, 'qqe_factor2': 1.5, 'threshold': 3,
                'bb_length': 20, 'bb_multi': 0.35
            },
            'SMA': {'periods': [50, 200]},
            'liquidity': {'swing_length': 64, 'range_percent': 0.1},
            'supertrend': {'period': 16, 'multiplier': 3},
            'TTM_squeeze': {
                'bb_length': 32, 'bb_std_dev': 2.0,
                'kc_length': 32, 'kc_mult': 1.5, 'use_true_range': True
            },
            'divergence_OBV': {'period': 128, 'lookback': 64},
            'divergence_Volume': {'period': 128, 'lookback': 64},
            'divergence_Fisher': {'period': 128, 'lookback': 64},
            'divergence_Vortex': {'period': 128, 'lookback': 64}
        },

         # 5min --------------------------------------------

        '5min': {
            'candle_colors': {
                'indicator_color': 'QQEMOD',
                'custom_params': {
                    'QQEMOD': {
                        'rsi_period': 10, 'rsi_period2': 5, 'sf': 10, 'sf2': 5,
                        'qqe_factor': 3.0, 'qqe_factor2': 1.61, 'threshold': 3,
                        'bb_length': 10, 'bb_multi': 0.35
                    }
                }
            },
            'aVWAP': {
                'peaks_valleys': False, 
                'peaks_valleys_avg': False,
                'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None},
                'OB': True, 
                'OB_avg': False,
                'OB_params': {'periods': 20, 'max_aVWAPs': 1},
                'gaps': False, 
                'gaps_avg': False,
                'gaps_params': {'max_aVWAPs': 10},
                'avg_lookback': 10, 
                'keep_OB_column': False
            },
            'OB': {'periods': 20},
            'StDev': {
                'centreline': 'peaks_valleys_avg',
                'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None},
                'std_lookback': 20, 'avg_lookback': 20
            },
            'QQEMOD': {
                'rsi_period': 10, 'rsi_period2': 5, 'sf': 10, 'sf2': 5,
                'qqe_factor': 3.0, 'qqe_factor2': 1.61, 'threshold': 3,
                'bb_length': 10, 'bb_multi': 0.35
            },
            'SMA': {'periods': [50, 100]},
            'liquidity': {'swing_length': 40, 'range_percent': 0.1},
            'supertrend': {'period': 20, 'multiplier': 3},
            'TTM_squeeze': {
                'bb_length': 40, 'bb_std_dev': 2.0,
                'kc_length': 40, 'kc_mult': 1.5, 'use_true_range': True
            },
            'divergence_OBV': {'period': 128, 'lookback': 80},
            'divergence_Volume': {'period': 128, 'lookback': 80},
            'divergence_Fisher': {'period': 128, 'lookback': 80},
            'divergence_Vortex': {'period': 128, 'lookback': 80}
        }
    }
}
