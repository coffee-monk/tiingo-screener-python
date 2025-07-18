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
            'weekly': ['OB_support'],
        },
        'params': {
            'OB_support': {
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

    'w_bankerRSI_d_OBSupport': {
        'criteria': {
            'weekly': ['banker_RSI'],
            'daily': ['OB_support'],
        },
        'params': {
            'OB_support': {
                'daily': {'atr_threshold_multiplier': 0.5}
            },
        },
    },

    'w_QQEMODOversold_d_OBullishZone': {
        'criteria': {
            'weekly': ['QQEMOD_oversold'],
            'daily': ['OB_bullish_aVWAP']
        },
        'params': {
            'OB_bullish_aVWAP': {
                'daily': {'distance_pct': 0.0, 'direction': 'below'}
            },
        },
    },

    'w_QQEMODOverbought_d_OBearishZone': {
        'criteria': {
            'weekly': ['QQEMOD_overbought'],
            'daily': ['OB_bearish_aVWAP']
        },
        'params': {
            'OB_bearish_aVWAP': {
                'daily': {'distance_pct': 0.0, 'direction': 'above'}
            },
        },
    },

    'w_supertrendBearish_d_OBullishZone': {
        'criteria': {
            'weekly': ['supertrend_bearish'],
            'daily': ['OB_bullish_aVWAP']
        },
        'params': {
            'OB_bullish_aVWAP': {
                'daily': {'distance_pct': 0.0, 'direction': 'below'}
            },
        },
    },

}
