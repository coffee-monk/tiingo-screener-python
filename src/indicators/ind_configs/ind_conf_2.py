# ind_conf_2

indicators = {  # aVWAP_channel = True

        'weekly': [
            'aVWAP', 
            'candle_colors', 
            'StDev', 
            'QQEMOD', 
            'banker_RSI',
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
            'OB',
            'TTM_squeeze',
            'divergence_Vortex', 'divergence_Fisher', 'divergence_OBV', 'divergence_Volume'
        ],

        '4hour': [
            'aVWAP', 
            'candle_colors',
            'StDev', 
            'QQEMOD', 
            'banker_RSI',
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
            'OB', 
            'TTM_squeeze', 
            'divergence_Vortex', 'divergence_Fisher', 'divergence_OBV', 'divergence_Volume'
        ],

        '5min': [
            'aVWAP', 
            'candle_colors', 
            'StDev', 
            'QQEMOD',
            'banker_RSI', 
            'OB', 
            'TTM_squeeze',
            'divergence_Vortex', 'divergence_Fisher', 'divergence_OBV', 'divergence_Volume'
        ]

}

params = {

        'weekly': {
            'candle_colors': {
                'indicator_color': 'StDev',
                'custom_params': {
                    'StDev': {
                        'std_lookback': 20, 'avg_lookback': 20,
                        'centreline': 'peaks_valleys_avg',
                        'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': 20}
                    },
                    'QQEMOD': {
                        'rsi_period': 8, 'rsi_period2': 8, 'sf': 6, 'sf2': 6,
                        'qqe_factor': 3.5, 'qqe_factor2': 2.0, 'threshold': 4,
                        'bb_length': 60, 'bb_multi': 0.4
                    }
                }
            },
            'aVWAP': {
                'peaks_valleys': True,
                'peaks_valleys_avg': False,
                'peaks_avg': True,
                'valleys_avg': True,
                'peaks_valleys_params': {'periods': 8, 'max_aVWAPs': None},
                'OB': True,
                'OB_avg': False,
                'OB_params': {'periods': 8, 'max_aVWAPs': None},
                'gaps': False,
                'gaps_avg': False,
                'gaps_params': {'max_aVWAPs': 8},
                'All_avg': False,
                'avg_lookback': 10,
                'keep_OB_column': False,
                'aVWAP_channel': True,
            },
            'OB': {'periods': 8},
            'StDev': {
                'centreline': 'peaks_valleys_avg',
                'peaks_valleys_params': {'periods': 8, 'max_aVWAPs': None},
                'std_lookback': 4, 'avg_lookback': 4
            },
            'QQEMOD': {
                'rsi_period': 8, 'rsi_period2': 8, 'sf': 6, 'sf2': 6,
                'qqe_factor': 3.5, 'qqe_factor2': 2.0, 'threshold': 4,
                'bb_length': 60, 'bb_multi': 0.4
            },
            'TTM_squeeze': {
                'bb_length': 20, 'bb_std_dev': 2.0,
                'kc_length': 20, 'kc_mult': 2.0, 'use_true_range': True
            },
            'divergence_OBV':    {'period': 26, 'lookback': 26},
            'divergence_Volume': {'period': 26, 'lookback': 26},
            'divergenCe_Fisher': {'period': 26, 'lookback': 26},
            'divergence_Vortex': {'period': 26, 'lookback': 26}
        },

        'daily': {
            'candle_colors': {
                'indicator_color': 'StDev',
                'custom_params': {
                    'StDev': {
                        'std_lookback': 20, 'avg_lookback': 20,
                        'centreline': 'peaks_valleys_avg',
                        'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None}
                    },
                    'QQEMOD': {
                        'rsi_period': 6, 'rsi_period2': 5, 'sf': 5, 'sf2': 5,
                        'qqe_factor': 3.0, 'qqe_factor2': 1.61, 'threshold': 3,
                        'bb_length': 50, 'bb_multi': 0.35
                    }
                }
            },
            'aVWAP': {
                'peaks_valleys': True,
                'peaks_valleys_avg': False,
                'peaks_avg': True,
                'valleys_avg': True,
                'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None},
                'OB': True,
                'OB_avg': False,
                'OB_params': {'periods': 20, 'max_aVWAPs': None},
                'gaps': False,
                'gaps_avg': False,
                'gaps_params': {'max_aVWAPs': 10},
                'All_avg': False,
                'avg_lookback': 20,
                'keep_OB_column': False,
                'aVWAP_channel': True,
            },
            'OB': {'periods': 20},
            'StDev': {
                'centreline': 'peaks_valleys_avg',
                'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None},
                'std_lookback': 20, 'avg_lookback': 20
            },
            'QQEMOD': {
                'rsi_period': 6, 'rsi_period2': 5, 'sf': 5, 'sf2': 5,
                'qqe_factor': 3.0, 'qqe_factor2': 1.61, 'threshold': 3,
                'bb_length': 50, 'bb_multi': 0.35
            },
            'TTM_squeeze': {
                'bb_length': 18, 'bb_std_dev': 1.9,
                'kc_length': 18, 'kc_mult': 1.7, 'use_true_range': True
            },
            'divergence_OBV':    {'period': 50, 'lookback': 50},
            'divergence_Volume': {'period': 50, 'lookback': 50},
            'divergence_Fisher': {'period': 50, 'lookback': 50},
            'divergence_Vortex': {'period': 50, 'lookback': 50}
        },

        '4hour': {
            'candle_colors': {
                'indicator_color': 'QQEMOD',
                'custom_params': {
                    'StDev': {
                        'centreline': 'peaks_valleys_avg',
                        'peaks_valleys_params': {'periods': 16, 'max_aVWAPs': None},
                        'std_lookback': 16, 'avg_lookback': 16
                    },
                    'QQEMOD': {
                        'rsi_period': 5, 'rsi_period2': 5, 'sf': 5, 'sf2': 4,
                        'qqe_factor': 2.5, 'qqe_factor2': 1.3, 'threshold': 2,
                        'bb_length': 40, 'bb_multi': 0.3
                    }
                }
            },
            'aVWAP': {
                'peaks_valleys': True,
                'peaks_valleys_avg': False,
                'peaks_avg': True,
                'valleys_avg': True,
                'peaks_valleys_params': {'periods': 30, 'max_aVWAPs': None},
                'OB': True,
                'OB_avg': False,
                'OB_params': {'periods': 30, 'max_aVWAPs': None},
                'gaps': False,
                'gaps_avg': False,
                'gaps_params': {'max_aVWAPs': 10},
                'All_avg': False,
                'avg_lookback': 20,
                'keep_OB_column': False,
                'aVWAP_channel': True,
            },
            'OB': {'periods': 30},
            'StDev': {
                'centreline': 'peaks_valleys_avg',
                'peaks_valleys_params': {'periods': 16, 'max_aVWAPs': None},
                'std_lookback': 16, 'avg_lookback': 16
            },
            'QQEMOD': {
                'rsi_period': 5, 'rsi_period2': 5, 'sf': 5, 'sf2': 4,
                'qqe_factor': 2.5, 'qqe_factor2': 1.3, 'threshold': 2,
                'bb_length': 40, 'bb_multi': 0.3
            },
            'TTM_squeeze': {
                'bb_length': 14, 'bb_std_dev': 1.8,
                'kc_length': 14, 'kc_mult': 1.3, 'use_true_range': True
            },
            'divergence_OBV':    {'period': 128, 'lookback': 64},
            'divergence_Volume': {'period': 128, 'lookback': 64},
            'divergence_Fisher': {'period': 128, 'lookback': 64},
            'divergence_Vortex': {'period': 128, 'lookback': 64}
        },

        '1hour': {
            'candle_colors': {
                'indicator_color': 'QQEMOD',
                'custom_params': {
                    'StDev': {
                        'centreline': 'peaks_valleys_avg',
                        'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None},
                        'std_lookback': 20, 'avg_lookback': 20
                    },
                    'QQEMOD': {
                        'rsi_period': 5, 'rsi_period2': 5, 'sf': 5, 'sf2': 4,
                        'qqe_factor': 2.5, 'qqe_factor2': 1.3, 'threshold': 2,
                        'bb_length': 40, 'bb_multi': 0.3
                    }
                }
            },
            'aVWAP': {
                'peaks_valleys': True,
                'peaks_valleys_avg': False,
                'peaks_avg': True,
                'valleys_avg': True,
                'peaks_valleys_params': {'periods': 25, 'max_aVWAPs': None},
                'OB': True,
                'OB_avg': False,
                'OB_params': {'periods': 25, 'max_aVWAPs': None},
                'gaps': False,
                'gaps_avg': False,
                'gaps_params': {'max_aVWAPs': 10},
                'All_avg': False,
                'avg_lookback': 25,
                'keep_OB_column': False,
                'aVWAP_channel': True,
            },
            'OB': {'periods': 25},
            'StDev': {
                'centreline': 'peaks_valleys_avg',
                'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None},
                'std_lookback': 20, 'avg_lookback': 20
            },
            'QQEMOD': {
                'rsi_period': 5, 'rsi_period2': 5, 'sf': 5, 'sf2': 4,
                'qqe_factor': 2.5, 'qqe_factor2': 1.3, 'threshold': 2,
                'bb_length': 40, 'bb_multi': 0.3
            },
            'TTM_squeeze': {
                'bb_length': 14, 'bb_std_dev': 1.8,
                'kc_length': 14, 'kc_mult': 1.3, 'use_true_range': True
            },
            'divergence_OBV':    {'period': 128, 'lookback': 64},
            'divergence_Volume': {'period': 128, 'lookback': 64},
            'divergence_Fisher': {'period': 128, 'lookback': 64},
            'divergence_Vortex': {'period': 128, 'lookback': 64}
        },

        '5min': {
            'candle_colors': {
                'indicator_color': 'QQEMOD',
                'custom_params': {
                    'StDev': {
                        'centreline': 'peaks_valleys_avg',
                        'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None},
                        'std_lookback': 20, 'avg_lookback': 20
                    },
                    'QQEMOD': {
                        'rsi_period': 4, 'rsi_period2': 4, 'sf': 3, 'sf2': 3,
                        'qqe_factor': 2.0, 'qqe_factor2': 1.0, 'threshold': 1.5,
                        'bb_length': 30, 'bb_multi': 0.25
                    }
                }
            },
            'aVWAP': {
                'peaks_valleys': True,
                'peaks_valleys_avg': False,
                'peaks_avg': True,
                'valleys_avg': True,
                'peaks_valleys_params': {'periods': 30, 'max_aVWAPs': None},
                'OB': True,
                'OB_avg': False,
                'OB_params': {'periods': 30, 'max_aVWAPs': None},
                'gaps': False,
                'gaps_avg': False,
                'gaps_params': {'max_aVWAPs': 10},
                'All_avg': False,
                'avg_lookback': 30,
                'keep_OB_column': False,
                'aVWAP_channel': True,
            },
            'OB': {'periods': 30},
            'StDev': {
                'centreline': 'peaks_valleys_avg',
                'peaks_valleys_params': {'periods': 20, 'max_aVWAPs': None},
                'std_lookback': 20, 'avg_lookback': 20
            },
            'QQEMOD': {
                'rsi_period': 4, 'rsi_period2': 4, 'sf': 3, 'sf2': 3,
                'qqe_factor': 2.0, 'qqe_factor2': 1.0, 'threshold': 1.5,
                'bb_length': 30, 'bb_multi': 0.25
            },
            'liquidity': {'swing_length': 40, 'range_percent': 0.1},
            'TTM_squeeze': {
                'bb_length': 12, 'bb_std_dev': 1.6,
                'kc_length': 12, 'kc_mult': 1.2, 'use_true_range': True
            },
            'divergence_OBV':    {'period': 128, 'lookback': 80},
            'divergence_Volume': {'period': 128, 'lookback': 80},
            'divergence_Fisher': {'period': 128, 'lookback': 80},
            'divergence_Vortex': {'period': 128, 'lookback': 80}
        }
}
