scan_conf = {

    # Weekly ==============================================

    'w_supertrendBullish_QQEMODOversold': {
        'criteria': {
            'weekly': ['supertrend', 'QQEMOD'],
        },
        'params': {
            'supertrend': {
                'weekly': {'mode': 'bullish'}
            }, 
            'QQEMOD': {
                'weekly': {'mode': 'oversold'}
            }, 
        },
    },

    'w_bankerRSI_QQEMODOversold': {
        'criteria': {
            'weekly': ['banker_RSI', 'QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                'weekly': {'mode': 'oversold'}
            }, 
        },
    },

    'w_bankerRSI': {
        'criteria': {
            'weekly': ['banker_RSI'],
        },
        'params': None
    },

    'w_OBSupport': {
        'criteria': {
            'weekly': ['OB'],
        },
        'params': {
            'OB': {
                'weekly': {'mode': 'support'}
            },
        },
    },

    'w_SMAAbove': {
        'criteria': {
            '1hour': ['SMA'],
        },
        'params': {
            'SMA': {
                '1hour': {'sma_periods': [200], 'distance_pct': 1.0, 'outside_range': True},
            }
        }
    },

    'w_SMABelow': {
        'criteria': {
            'weekly': ['SMA'],
        },
        'params': {
            'SMA': {
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
            'weekly': ['QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                'weekly': {'mode': 'bullish_reversal'},
            }
        }
    },

    'w_QQEMODBearishReversal': {
        'criteria': {
            'weekly': ['QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                'weekly': {'mode': 'bearish_reversal'},
            }
        }
    },

    # Weekly + Daily ======================================

    'w_bankerRSI_d_OBSupport': {
        'criteria': {
            'weekly': ['banker_RSI'],
            'daily': ['OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'support'}
            },
        },
    },

    'w_QQEMODOversold_d_OBullishZone': {
        'criteria': {
            'weekly': ['QQEMOD'],
            'daily': ['OB_aVWAP']
        },
        'params': {
            'QQEMOD': {
                'weekly': {'mode': 'oversold'}
            },
            'OB_aVWAP': {
                'daily': {'mode': 'bullish', 'direction': 'below'}
            },
        },
    },

    'w_QQEMODOverbought_d_OBearishZone': {
        'criteria': {
            'weekly': ['QQEMOD_overbought'],
            'daily': ['OB_aVWAP']
        },
        'params': {
            'QQEMOD': {
                'daily': {'mode': 'overbought'}
            },
            'OB_aVWAP': {
                'daily': {'mode': 'bearish', 'direction': 'above'}
            },
        },
    },

    'w_OscVol': {
        'criteria': {
            'weekly': ['oscillation_volatility'],
        },
        'params': {
            'oscillation_volatility': {
                'weekly': {'cross_count': 1, 'avg_deviation': 0.0, 'oscillation_score': 3.0},
            }
        }
    },

}
