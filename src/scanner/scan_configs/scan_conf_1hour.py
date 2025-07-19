scan_conf = {

    # 1hour ==============================================

    'h_aVWAPChannelOverbought': {
        'criteria': {
            '1hour': ['aVWAP_channel_resistance'],
        },
        'params': {
            'aVWAP_channel_resistance': {
                '1hour': {'distance_pct': 10.0, 'direction': 'above'}
            },
        }
    },

    'h_aVWAPChannelOversold': {
        'criteria': {
            '1hour': ['aVWAP_channel_support'],
        },
        'params': {
            'aVWAP_channel_support': {
                '1hour': {'distance_pct': 10.0, 'direction': 'below'}
            },
        }
    },

    'h_aVWAPChannelResistance': {
        'criteria': {
            '1hour': ['aVWAP_channel_resistance'],
        },
        'params': {
            'aVWAP_channel_resistance': {
                '1hour': {'distance_pct': 5.0, 'direction': 'within'}
            },
        }
    },

    'h_aVWAPChannelSupport': {
        'criteria': {
            '1hour': ['aVWAP_channel_support'],
        },
        'params': {
            'aVWAP_channel_support': {
                '1hour': {'distance_pct': 5.0, 'direction': 'within'}
            },
        }
    },

    'h_aVWAPPeaksavg': {
        'criteria': {
            '1hour': ['aVWAP_peaks_avg'],
        },
        'params': {
            'aVWAP_peaks_avg': {
                '1hour': {'distance_pct': 1.0, 'direction': 'within'}
            },
        }
    },

    'h_aVWAPValleysavg': {
        'criteria': {
            '1hour': ['aVWAP_valleys_avg'],
        },
        'params': {
            'aVWAP_valleys_avg': {
                '1hour': {'distance_pct': 1.0, 'direction': 'within'}
            },
        }
    },

    'h_StDevOversold_OBSupport': {
        'criteria': {
            '1hour': ['StDev_oversold', 'OB_support'],
        },
        'params': {
            'StDev_oversold': {
                '1hour': {'threshold': 2}
            },
        }
    },

    'h_OBSupport': {
        'criteria': {
            '1hour': ['OB_support'],
        },
        'params': {
            'OB_support': {
                '1hour': {'atr_threshold_multiplier': None}
            },
        }
    },

    'h_OBResistance': {
        'criteria': {
            '1hour': ['OB_resistance'],
        },
        'params': {
            'OB_resistance': {
                '1hour': {'atr_threshold_multiplier': None}
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

    'h_aVWAPavgBelow_OBBullish': {
        'criteria': {
            '1hour': ['aVWAP_avg', 'OB_bullish'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {
                          'direction': 'below',
                          'distance_pct': 1.0, 
                          'outside_range': True
                },
            }
        }
    },

}
