scan_conf = {

    # Daily ===============================================

    'd_aVWAPChannelOverbought': {
        'criteria': {
            'daily': ['aVWAP_channel_resistance'],
        },
        'params': {
            'aVWAP_channel_resistance': {
                'daily': {'distance_pct': 10.0, 'direction': 'above'}
            },
        }
    },

    'd_aVWAPChannelOversold': {
        'criteria': {
            'daily': ['aVWAP_channel_support'],
        },
        'params': {
            'aVWAP_channel_support': {
                'daily': {'distance_pct': 10.0, 'direction': 'below'}
            },
        }
    },

    'd_aVWAPChannelResistance': {
        'criteria': {
            'daily': ['aVWAP_channel_resistance'],
        },
        'params': {
            'aVWAP_channel_resistance': {
                'daily': {'distance_pct': 5.0, 'direction': 'within'}
            },
        }
    },

    'd_aVWAPChannelSupport': {
        'criteria': {
            'daily': ['aVWAP_channel_support'],
        },
        'params': {
            'aVWAP_channel_support': {
                'daily': {'distance_pct': 5.0, 'direction': 'within'}
            },
        }
    },

    'd_aVWAPPeaksavg': {
        'criteria': {
            'daily': ['aVWAP_peaks_avg'],
        },
        'params': {
            'aVWAP_peaks_avg': {
                'daily': {'distance_pct': 1.0, 'direction': 'within'}
            },
        }
    },

    'd_aVWAPValleysavg': {
        'criteria': {
            'daily': ['aVWAP_valleys_avg'],
        },
        'params': {
            'aVWAP_valleys_avg': {
                'daily': {'distance_pct': 1.0, 'direction': 'within'}
            },
        }
    },

    'd_StDevOversold_OBSupport': {
        'criteria': {
            'daily': ['StDev_oversold', 'OB_support'],
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
            'daily': ['QQEMOD_oversold', 'OB_support'],
        },
        'params': {
            'OB_support': {
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
                'daily': {
                          'direction': 'within',
                          'distance_pct': 1.0, 
                          'outside_range': False
                         },
            }
        }
    },

    'd_aVWAPavgAbove': {
        'criteria': {
            'daily': ['aVWAP_avg'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {
                          'direction': 'within',
                          'distance_pct': 20.0, 
                          'outside_range': False
                },
            }
        }
    },

    'd_aVWAPavgBelow': {
        'criteria': {
            'daily': ['aVWAP_avg'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {
                          'direction': 'below',
                          'distance_pct': 20.0, 
                          'outside_range': False
                },
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

    'd_aVWAPavgBelow_OBBullish': {
        'criteria': {
            'daily': ['aVWAP_avg', 'OB_bullish'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {
                          'direction': 'below',
                          'distance_pct': 1.0, 
                          'outside_range': True
                },
            },
        }
    },

    # Daily + 1hour =======================================

    'd_DivBullish_h_DivBullish': {
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

    'd_DivBearish_h_DivBearish': {
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

    'd_StDevOversold_h_OBSupport': {
        'criteria': {
            'daily': ['StDev_oversold'],
            '1hour': ['OB_support']
        },
        'params': {
            'StDev_oversold': {
                'daily': {'threshold': 2}
            },
            'OB_support': {
                '1hour': {'atr_threshold_multiplier': 1.0}
            },
        }
    },

    'd_StDevOverbought_h_OBResistance': {
        'criteria': {
            'daily': ['StDev_overbought'],
            '1hour': ['OB_resistance']
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

    'd_OBSupport_h_OBSupport': {
        'criteria': {
            'daily': ['OB_support'],
            '1hour': ['OB_support']
        },
        'params': {
            'OB_support': {
                'daily': {'atr_threshold_multiplier': 1.5},
                '1hour': {'atr_threshold_multiplier': 1.5}
            },
        }
    },

    'd_OBResistance_h_OBResistance': {
        'criteria': {
            'daily': ['OB_resistance'],
            '1hour': ['OB_resistance']
        },
        'params': {
            'OB_resistance': {
                'daily': {'atr_threshold_multiplier': 1.5},
                '1hour': {'atr_threshold_multiplier': 1.5}
            },
        }
    },

    'd_SMA_h_SMA': {
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

    'd_OBBullishaVWAP': {
        'criteria': {
            'daily': ['OB_bullish_aVWAP'],
        },
        'params': {
            'OB_bullish_aVWAP': {
                'daily': {'distance_pct': 1.0, 'direction': 'within'},
            }
        }
    },

    'd_OBBearishaVWAP': {
        'criteria': {
            'daily': ['OB_bearish_aVWAP'],
        },
        'params': {
            'OB_bearish_aVWAP': {
                'daily': {'distance_pct': 1.0, 'direction': 'within'},
            }
        }
    },

}

