# Custom Inputs for run_scanner() =========================

scan_configs = {

    # Daily ===============================================

    'd_StDevOversold_OBSupport': {
        'criteria': {
            'daily': ['StDev_oversold', 'OB_bullish_support'],
        },
        'params': {
            'StDev_oversold': {
                'daily': {'threshold': 2}
            },
        }
    },

    'd_StDevOverbought_OBResistance': {
        'criteria': {
            'daily': ['StDev_overbought'],
        },
        'params': {
            'StDev_oversold': {
                'daily': {'threshold': 2}
            },
        }
    },

    'd_QQEMODOversold_OBSupport': {
        'criteria': {
            'daily': ['QQEMOD_oversold', 'OB_bullish_support'],
        },
        'params': {
            'OB_bullish_support': {
                'daily': {'atr_threshold_multiplier': 0.5}
            },
        }
    },

    'd_supertrendBullish_QQEMODOversold': {
        'criteria': {
            'daily': ['supertrend_bullish', 'QQEMOD_oversold'],
        },
    },

    'd_bankerRSI_QQEMODOversold': {
        'criteria': {
            'daily': ['banker_RSI', 'QQEMOD_oversold'],
        },
    },

    # Daily + 1hour =======================================

    # dh_OBBullish_support 
    # dh_OBBearish_resistance

    'dh_OB_support': {
        'criteria': {
            'daily': ['OB_bullish_below_aVWAP'],
            '1hour': ['OB_bullish_support']
        },
        'params': {
            'OB_bullish_support': {
                '1hour': {'atr_threshold_multiplier': 0.5}
            }
        }
    },

    'dh_OB_resistance': {
        'criteria': {
            'daily': ['OB_bearish_above_aVWAP'],
            '1hour': ['OB_bearish_resistance']
        },
        'params': {
            'OB_bearish_resistance': {
                '1hour': {'resistance_threshold': 0.5}
            }
        }
    },

    # divergences_bullish 
    # divergences_bearish

    'dh_divergences_bullish': {
        'criteria': {
            'daily': ['divergences_bullish'],
            '1hour': ['divergences_bullish']
        },
        'params': {
            'divergences_bullish': {
                '1hour': {'max_bars_back': 20}
            }
        }
    },

    'dh_divergences_bearish': {
        'criteria': {
            'daily': ['divergences_bearish'],
            '1hour': ['divergences_bearish']
        },
        'params': {
            'divergences_bearish': {
                '1hour': {'max_bars_back': 20}
            }
        }
    },

    # dh_StDev_oversold_OBBullish
    # dh_StDev_overbought_OBBearish

    'dh_StDevOversold_OBBSupport': {
        'criteria': {
            'daily': ['StDev_oversold'],
            '1hour': ['OB_bullish_support']
        },
        'params': {
            'StDev_oversold': {
                'daily': {'threshold': 2}
            },
            'OB_bullish_support': {
                '1hour': {'atr_threshold_multiplier': 1.0}
            },
        }
    },

    'dh_StDevOverbought_OBResistance': {
        'criteria': {
            'daily': ['StDev_overbought'],
            '1hour': ['OB_bearish_resistance']
        },
        'params': {
            'StDev_oversold': {
                'daily': {'threshold': 2}
            },
            'OB_bullish_resistance': {
                '1hour': {'atr_threshold_multiplier': 1.0}
            },
        }
    },

    # Weekly + Daily ======================================

    'wd_QQEMODOversold_OBBullishZone': {
        'criteria': {
            'weekly': ['QQEMOD_oversold'],
            'daily': ['OB_bullish_below_aVWAP']
        },
    },

    'wd_QQEMODOverbought_OBBearishZone': {
        'criteria': {
            'weekly': ['QQEMOD_overbought'],
            'daily': ['OB_bearish_above_aVWAP']
        },
    },

    'wd_supertrendBearish_OBBullishZone': {
        'criteria': {
            'weekly': ['supertrend_bearish'],
            'daily': ['OB_bullish_below_aVWAP']
        },
    },

    # Weekly ==============================================

    'w_supertrendBullish_QQEMODOversold': {
        'criteria': {
            'weekly': ['supertrend_bullish', 'QQEMOD_oversold'],
        },
    },


}
