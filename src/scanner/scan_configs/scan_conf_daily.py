scan_conf = {

    # Daily ===============================================

    'd_aVWAPChannelOverbought': {
        'criteria': {
            'daily': ['aVWAP_channel'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'resistance', 'direction': 'above'}
            },
        }
    },

    'd_aVWAPChannelOversold': {
        'criteria': {
            'daily': ['aVWAP_channel'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'support', 'direction': 'below'}
            },
        }
    },

    'd_aVWAPChannelResistance': {
        'criteria': {
            'daily': ['aVWAP_channel'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'resistance', 'direction': 'within'}
            },
        }
    },

    'd_aVWAPChannelSupport': {
        'criteria': {
            'daily': ['aVWAP_channel'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'support', 'direction': 'within'}
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

    'd_OBBullish': {
        'criteria': {
            'daily': ['OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'bullish'}
            },
        }
    },

    'd_OBBearish': {
        'criteria': {
            'daily': ['OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'bearish'}
            },
        }
    },

    'd_OBSupport': {
        'criteria': {
            'daily': ['OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'support'}
            },
        }
    },

    'd_OBResistance': {
        'criteria': {
            'daily': ['OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'resistance'}
            },
        }
    },

    'd_StDevOversold_OBSupport': {
        'criteria': {
            'daily': ['StDev', 'OB'],
        },
        'params': {
            'StDev': {
                'daily': {'threshold': 2, 'mode': 'overbought'}
            },
            'OB': {
                'daily': {'mode': 'support'}
            },
        }
    },

    'd_StDevOverbought_OBResistance': {
        'criteria': {
            'daily': ['StDev', 'OB'],
        },
        'params': {
            'StDev': {
                'daily': {'threshold': 2, 'mode': 'overbought'}
            },
            'OB': {
                'daily': {'mode': 'resistance'}
            },
        }
    },

    'd_QQEMODOversold_OBSupport': {
        'criteria': {
            'daily': ['QQEMOD', 'OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'support'}
            },
            'QQEMOD': {
                'daily': {'mode': 'oversold'}
            },
        }
    },

    'd_supertrendBullish_QQEMODOversold': {
        'criteria': {
            'daily': ['supertrend', 'QQEMOD'],
        },
        'params': {
            'supertrend': {
                'daily': {'mode': 'bullish'},
            },
            'QQEMOD': {
                'daily': {'mode': 'oversold'},
            }
        }
    },

    'd_bankerRSI_QQEMODOversold': {
        'criteria': {
            'daily': ['banker_RSI', 'QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                'daily': {'mode': 'oversold'},
            }
        }
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
            'daily': ['SMA'],
        },
        'params': {
            'SMA': {
                'daily': {'sma_periods': [200], 
                          'mode': 'above', 
                          'distance_pct': 30.0, 
                          'outside_range': True},
            }
        }
    },

    'd_SMABelow': {
        'criteria': {
            'daily': ['SMA'],
        },
        'params': {
            'SMA': {
                'daily': {'sma_periods': [200], 
                          'mode': 'below', 
                          'distance_pct': 30.0, 
                          'outside_range': True},
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
                          'direction': 'above',
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

    'd_QQEMODOverbought': {
        'criteria': {
            'daily': ['QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                'daily': {'mode': 'overbought'},
            }
        }
    },

    'd_QQEMODOversold': {
        'criteria': {
            'daily': ['QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                'daily': {'mode': 'oversold'},
            }
        }
    },

    'd_aVWAPavgBelow_OBBullish': {
        'criteria': {
            'daily': ['aVWAP_avg', 'OB'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {
                          'direction': 'below',
                          'distance_pct': 1.0, 
                          'outside_range': True
                },
            },
            'OB': {
                'daily': {'mode': 'bullish'},
            },
        }
    },

    'd_DivBullish': {
        'criteria': {
            'daily': ['divergences'],
        },
        'params': {
            'divergences': {
                'daily': {'mode': 'bullish', 'max_bars_back': 100},
            }
        }
    },

    'd_DivBearish': {
        'criteria': {
            'daily': ['divergences'],
        },
        'params': {
            'divergences': {
                'daily': {'mode': 'bearish', 'max_bars_back': 100},
            }
        }
    },

    # Daily + 1hour =======================================

    'd_DivBullish_h_DivBullish': {
        'criteria': {
            'daily': ['divergences'],
            '1hour': ['divergences']
        },
        'params': {
            'divergences': {
                'daily': {'mode': 'bullish', 'max_bars_back': 20},
                '1hour': {'mode': 'bullish', 'max_bars_back': 20}
            }
        }
    },

    'd_DivBearish_h_DivBearish': {
        'criteria': {
            'daily': ['divergences'],
            '1hour': ['divergences']
        },
        'params': {
            'divergences': {
                'daily': {'mode': 'bearish', 'max_bars_back': 20},
                '1hour': {'mode': 'bearish', 'max_bars_back': 20}
            }
        }
    },

    'd_StDevOversold_h_OBSupport': {
        'criteria': {
            'daily': ['StDev'],
            '1hour': ['OB']
        },
        'params': {
            'StDev': {
                'daily': {'mode': 'oversold', 'threshold': 2}
            },
            'OB': {
                '1hour': {'mode': 'support'}
            },
        }
    },

    'd_StDevOverbought_h_OBResistance': {
        'criteria': {
            'daily': ['StDev'],
            '1hour': ['OB']
        },
        'params': {
            'StDev': {
                'daily': {'mode': 'overbought', 'threshold': 2}
            },
            'OB': {
                '1hour': {'mode': 'resistance', 'atr_threshold_multiplier': 1.0}
            },
        }
    },

    'd_OBSupport_h_OBSupport': {
        'criteria': {
            'daily': ['OB'],
            '1hour': ['OB']
        },
        'params': {
            'OB': {
                'daily': {'mode': 'support', 'atr_threshold_multiplier': 1.5},
                '1hour': {'mode': 'support', 'atr_threshold_multiplier': 1.5}
            },
        }
    },

    'd_OBResistance_h_OBResistance': {
        'criteria': {
            'daily': ['OB'],
            '1hour': ['OB']
        },
        'params': {
            'OB': {
                'daily': {'mode': 'resistance', 'atr_threshold_multiplier': 1.5},
                '1hour': {'mode': 'resistance', 'atr_threshold_multiplier': 1.5}
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
            'daily': ['OB_aVWAP'],
        },
        'params': {
            'OB_aVWAP': {
                'daily': {'bullish': 'bullish', 'distance_pct': 1.0, 'direction': 'within'},
            }
        }
    },

    'd_OBBearishaVWAP': {
        'criteria': {
            'daily': ['OB_aVWAP'],
        },
        'params': {
            'OB_aVWAP': {
                'daily': {'mode': 'bearish', 'distance_pct': 1.0, 'direction': 'within'},
            }
        }
    },

}
