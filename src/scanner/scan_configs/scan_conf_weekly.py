scan_conf = {

    # Weekly ==============================================

    'w_supertrendBullish_QQEMODOversold': {
        'criteria': {
            'weekly': ['supertrend_bullish', 'QQEMOD_oversold'],
        },
        'params': None
    },

    'w_bankerRSI_QQEMODOversold': {
        'criteria': {
            'weekly': ['banker_RSI', 'QQEMOD_oversold'],
        },
        'params': None
    },

    'w_bankerRSI': {
        'criteria': {
            'weekly': ['banker_RSI'],
        },
        'params': None
    },

    'w_OBSupport': {
        'criteria': {
            'weekly': ['OB_bullish_support'],
        },
        'params': {
            'OB_bullish_support': {
                'weekly': {'atr_threshold_multiplier': 0.5}
            },
        },
    },

    'w_SMAAbove': {
        'criteria': {
            '1hour': ['SMA_above'],
        },
        'params': {
            'SMA_above': {
                '1hour': {'sma_periods': [200], 'distance_pct': 1.0, 'outside_range': True},
            }
        }
    },

    'w_SMABelow': {
        'criteria': {
            'weekly': ['SMA_below'],
        },
        'params': {
            'SMA_below': {
                'weekly': {'sma_periods': [200], 'distance_pct': 1.0, 'outside_range': True},
            }
        }
    },

    'w_TTMSqueeze': {
        'criteria': {
            'weekly': ['TTM_squeeze'],
        },
        'params': {
            'TTM_squeeze': {
                'weekly': {'min_squeeze_bars': 5, 'max_squeeze_bars': None},
            }
        }
    },

    'w_QQEMODBullishReversal': {
        'criteria': {
            'weekly': ['QQEMOD_bullish_reversal'],
        },
        'params': {
            'QQEMOD_bullish_reversal': {
                'weekly': {'min_red_candles': 3},
            }
        }
    },

    'w_QQEMODBearishReversal': {
        'criteria': {
            'weekly': ['QQEMOD_bearish_reversal'],
        },
        'params': {
            'QQEMOD_bearish_reversal': {
                'weekly': {'min_red_candles': 3},
            }
        }
    },

    # Weekly + Daily ======================================

    'wd_bankerRSI_OBSupport': {
        'criteria': {
            'weekly': ['banker_RSI'],
            'daily': ['OB_bullish_support'],
        },
        'params': {
            'OB_bullish_support': {
                'daily': {'atr_threshold_multiplier': 0.5}
            },
        },
    },

    'wd_QQEMODOversold_OBullishZone': {
        'criteria': {
            'weekly': ['QQEMOD_oversold'],
            'daily': ['OB_bullish_below_aVWAP']
        },
        'params': None
    },

    'wd_QQEMODOverbought_OBearishZone': {
        'criteria': {
            'weekly': ['QQEMOD_overbought'],
            'daily': ['OB_bearish_above_aVWAP']
        },
        'params': None
    },

    'wd_supertrendBearish_OBullishZone': {
        'criteria': {
            'weekly': ['supertrend_bearish'],
            'daily': ['OB_bullish_below_aVWAP']
        },
        'params': None
    },

}
