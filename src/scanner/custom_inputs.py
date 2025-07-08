# Custom Inputs for run_scanner() =========================

scan_configs = {

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
        'params': None
    },

    'd_bankerRSI_QQEMODOversold': {
        'criteria': {
            'daily': ['banker_RSI', 'QQEMOD_oversold'],
        },
        'params': None
    },

    'd_SMA': {
        'criteria': {
            'daily': ['SMA'],
        },
        'params': {
            'SMA': {
                'daily': {'sma_periods': [50], 'distance_pct': 1.0},
            }
        }
    },

    'd_SMAAbove': {
        'criteria': {
            'daily': ['SMA_above'],
        },
        'params': {
            'SMA_above': {
                'daily': {'sma_periods': [200], 'distance_pct': 30.0, 'outside_range': True},
            }
        }
    },

    'd_SMABelow': {
        'criteria': {
            'daily': ['SMA_below'],
        },
        'params': {
            'SMA_below': {
                'daily': {'sma_periods': [200], 'distance_pct': 30.0, 'outside_range': True},
            }
        }
    },

    'd_aVWAPavg': {
        'criteria': {
            'daily': ['aVWAP_avg'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {'distance_pct': 1.0},
            }
        }
    },

    'd_aVWAPavgAbove': {
        'criteria': {
            'daily': ['aVWAP_avg_above'],
        },
        'params': {
            'aVWAP_avg_above': {
                'daily': {'distance_pct': 20.0, 'outside_range': False},
            }
        }
    },

    'd_aVWAPavgBelow': {
        'criteria': {
            'daily': ['aVWAP_avg_below'],
        },
        'params': {
            'aVWAP_avg_below': {
                'daily': {'distance_pct': 20.0, 'outside_range': False},
            }
        }
    },

    'd_TTMSqueeze': {
        'criteria': {
            'daily': ['TTM_squeeze'],
        },
        'params': {
            'TTM_squeeze': {
                'daily': {'min_squeeze_bars': 5, 'max_squeeze_bars': None},
            }
        }
    },

    'd_QQEMODBullishReversal': {
        'criteria': {
            'daily': ['QQEMOD_bullish_reversal'],
        },
        'params': {
            'QQEMOD_bullish_reversal': {
                'daily': {'min_red_candles': 3},
            }
        }
    },

    'd_QQEMODBearishReversal': {
        'criteria': {
            '1hour': ['QQEMOD_bearish_reversal'],
        },
        'params': {
            'QQEMOD_bearish_reversal': {
                '1hour': {'min_red_candles': 3},
            }
        }
    },

    # Daily + 1hour =======================================

    ' dh_divergences_bullish': {
        'criteria': {
            'daily': ['divergences_bullish'],
            '1hour': ['divergences_bullish']
        },
        'params': {
            'divergences_bullish': {
                'daily': {'max_bars_back': 20},
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
                'daily': {'max_bars_back': 20},
                '1hour': {'max_bars_back': 20}
            }
        }
    },

    'dh_StDevOversold_OBSupport': {
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

    'dh_OBSupport': {
        'criteria': {
            'daily': ['OB_bullish_support'],
            '1hour': ['OB_bullish_support']
        },
        'params': {
            'OB_bullish_support': {
                'daily': {'atr_threshold_multiplier': 1.5},
                '1hour': {'atr_threshold_multiplier': 1.5}
            },
        }
    },

    'dh_OBResistance': {
        'criteria': {
            'daily': ['OB_bearish_resistance'],
            '1hour': ['OB_bearish_resistance']
        },
        'params': {
            'OB_bearish_resistance': {
                'daily': {'atr_threshold_multiplier': 1.5},
                '1hour': {'atr_threshold_multiplier': 1.5}
            },
        }
    },

    'dh_SMA': {
        'criteria': {
            'daily': ['SMA'],
            '1hour': ['SMA'],
        },
        'params': {
            'SMA': {
                'daily': {'sma_periods': [50], 'distance_pct': 1.0},
                '1hour': {'sma_periods': [50], 'distance_pct': 1.0},
            }
        }
    },

    # 1hour ==============================================

    'h_StDevOversold_OBSupport': {
        'criteria': {
            '1hour': ['StDev_oversold', 'OB_bullish_support'],
        },
        'params': {
            'StDev_oversold': {
                '1hour': {'threshold': 2}
            },
        }
    },

    'h_OBSupport': {
        'criteria': {
            '1hour': ['OB_bullish_support'],
        },
        'params': {
            'OB_bullish_support': {
                '1hour': {'atr_threshold_multiplier': 0.5}
            },
        }
    },

    'h_supertrendBullish_QQEMODOversold': {
        'criteria': {
            '1hour': ['supertrend_bullish', 'QQEMOD_oversold'],
        },
        'params': None
    },

    'h_bankerRSI_QQEMODOversold': {
        'criteria': {
            '1hour': ['banker_RSI', 'QQEMOD_oversold'],
        },
        'params': None
    },

    'h_SMA': {
        'criteria': {
            '1hour': ['SMA'],
        },
        'params': {
            'SMA': {
                '1hour': {'sma_periods': [50], 'distance_pct': 1.0},
            }
        }
    },

    'h_SMAAbove': {
        'criteria': {
            '1hour': ['SMA_above'],
        },
        'params': {
            'SMA_above': {
                '1hour': {'sma_periods': [200], 'distance_pct': 1.0, 'outside_range': False},
            }
        }
    },

    'h_SMABelow': {
        'criteria': {
            '1hour': ['SMA_below'],
        },
        'params': {
            'SMA_below': {
                '1hour': {'sma_periods': [200], 'distance_pct': 1.0, 'outside_range': False},
            }
        }
    },

    'h_TTMSqueeze': {
        'criteria': {
            '1hour': ['TTM_squeeze'],
        },
        'params': {
            'TTM_squeeze': {
                '1hour': {'min_squeeze_bars': 5, 'max_squeeze_bars': None},
            }
        }
    },

    'h_QQEMODBullishReversal': {
        'criteria': {
            '1hour': ['QQEMOD_bullish_reversal'],
        },
        'params': {
            'QQEMOD_bullish_reversal': {
                '1hour': {'min_red_candles': 3},
            }
        }
    },

    'h_QQEMODBearishReversal': {
        'criteria': {
            '1hour': ['QQEMOD_bearish_reversal'],
        },
        'params': {
            'QQEMOD_bearish_reversal': {
                '1hour': {'min_red_candles': 3},
            }
        }
    },

}
