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
                'daily': {'mode': 'resistance', 'direction': 'within', 'distance_pct': 1.0}
            },
        }
    },

    'd_aVWAPChannelSupport': {
        'criteria': {
            'daily': ['aVWAP_channel'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'support', 'direction': 'within', 'distance_pct': 1.0}
            },
        }
    },

    'd_aVWAPChannelSupport_OBSupport': {
        'criteria': {
            'daily': ['aVWAP_channel', 'OB'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'support', 'distance_pct': 5.0}
            },
            'OB': {
                'daily': {'mode': 'support'}
            },
        }
    },

    'd_aVWAPChannelResistance_OBResistance': {
        'criteria': {
            'daily': ['aVWAP_channel', 'OB'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'resistance', 'distance_pct': 5.0}
            },
            'OB': {
                'daily': {'mode': 'resistance'}
            },
        }
    },

    'd_aVWAPChannelSupport_aVWAPPeaksavg': {
        'criteria': {
            'daily': ['aVWAP_channel', 'aVWAP_avg'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'support', 'direction': 'within', 'distance_pct': 1.0}
            },
            'aVWAP_avg': {
                'daily': {
                          'mode': 'peaks', 
                          'direction': 'within', 
                          'distance_pct': 0.5, 
                         }
            },
        }
    },

    'd_aVWAPChannelSupport_aVWAPValleysavg': {
        'criteria': {
            'daily': ['aVWAP_channel', 'aVWAP_avg'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'support', 'direction': 'within', 'distance_pct': 1.0}
            },
            'aVWAP_avg': {
                'daily': {
                          'mode': 'valleys', 
                          'direction': 'within', 
                          'distance_pct': 0.5, 
                         }
            },
        }
    },

    'd_aVWAPChannelResistance_aVWAPValleysavg': {
        'criteria': {
            'daily': ['aVWAP_channel', 'aVWAP_avg'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'resistance', 'direction': 'within', 'distance_pct': 1.0}
            },
            'aVWAP_avg': {
                'daily': {
                          'mode': 'valleys', 
                          'direction': 'within', 
                          'distance_pct': 1.0, 
                         }
            },
        }
    },

    'd_aVWAPChannelResistance_aVWAPPeaksavg': {
        'criteria': {
            'daily': ['aVWAP_channel', 'aVWAP_avg'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {'mode': 'resistance', 'direction': 'within', 'distance_pct': 1.0}
            },
            'aVWAP_avg': {
                'daily': {
                          'mode': 'peaks', 
                          'direction': 'within', 
                          'distance_pct': 0.5, 
                         }
            },
        }
    },

    'd_aVWAPPeaksavg': {
        'criteria': {
            'daily': ['aVWAP_avg'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {
                          'mode': 'peaks', 
                          'direction': 'above', 
                          'distance_pct': 1.0, 
                         }
            },
        }
    },

    'd_aVWAPValleysavg': {
        'criteria': {
            'daily': ['aVWAP_avg'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {
                          'mode': 'valleys',
                          'direction': 'below',
                          'distance_pct': 1.0, 
                         }
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

    'd_OBOversold': {
        'criteria': {
            'daily': ['OB'],
        },
        'params': {
            'OB': {
                'daily': {
                          'mode': 'bullish',
                          'stdev_mode': 'oversold',
                          'stdev_threshold': 1.5,
                          'max_lookback': 15,
                         }
            },
        }
    },

    'd_OBOverbought': {
        'criteria': {
            'daily': ['OB'],
        },
        'params': {
            'OB': {
                'daily': {
                          'mode': 'bearish', 
                          'stdev_mode': 'overbought', 
                          'stdev_threshold': 1.5,
                          'max_lookback': 25,
                         }
            },
        }
    },

    'd_StDevOversold_OBSupport': {
        'criteria': {
            'daily': ['StDev', 'OB'],
        },
        'params': {
            'StDev': {
                'daily': {'threshold': 1.5, 'mode': 'oversold'}
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
                'daily': {'threshold': 1.5, 'mode': 'overbought'}
            },
            'OB': {
                'daily': {'mode': 'resistance'}
            },
        }
    },

    'd_StDevOversold_OBBullish': {
        'criteria': {
            'daily': ['StDev', 'OB'],
        },
        'params': {
            'StDev': {
                'daily': {'threshold': 1.5, 'mode': 'oversold'}
            },
            'OB': {
                'daily': {'mode': 'bullish'}
            },
        }
    },

    'd_StDevOverbought_OBBearish': {
        'criteria': {
            'daily': ['StDev', 'OB'],
        },
        'params': {
            'StDev': {
                'daily': {'threshold': 1.5, 'mode': 'overbought'}
            },
            'OB': {
                'daily': {'mode': 'bearish'}
            },
        }
    },

    'd_QQEMODBullishReversal': {
        'criteria': {
            '4hour': ['QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                '4hour': {'mode': 'bullish_reversal'},
            }
        }
    },

    'd_QQEMODBearishReversal': {
        'criteria': {
            'daily': ['QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                'daily': {'mode': 'bearish_reversal'},
            }
        }
    },

    'd_QQEMODOverbought_OBResistance': {
        'criteria': {
            'daily': ['QQEMOD', 'OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'resistance'}
            },
            'QQEMOD': {
                'daily': {'mode': 'overbought'}
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

    'd_QQEMODOversold_OBResistance': {
        'criteria': {
            'daily': ['QQEMOD', 'OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'resistance'}
            },
            'QQEMOD': {
                'daily': {'mode': 'oversold'}
            },
        }
    },

    'd_QQEMODOverbought_OBSupport': {
        'criteria': {
            'daily': ['QQEMOD', 'OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'support'}
            },
            'QQEMOD': {
                'daily': {'mode': 'overbought'}
            },
        }
    },

    'd_QQEMODBullishReversal_OBResistance': {
        'criteria': {
            'daily': ['QQEMOD', 'OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'resistance'}
            },
            'QQEMOD': {
                'daily': {'mode': 'bullish_reversal'}
            },
        }
    },

    'd_QQEMODBearishReversal_OBSupport': {
        'criteria': {
            'daily': ['QQEMOD', 'OB'],
        },
        'params': {
            'OB': {
                'daily': {'mode': 'support'}
            },
            'QQEMOD': {
                'daily': {'mode': 'bearish_reversal'}
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
                          'distance_pct': 5.0, 
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
                          'distance_pct': 5.0, 
                          'outside_range': True
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
                          'distance_pct': 5.0, 
                          'outside_range': True
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

    'd_aVWAPavgAbove_OBBearish': {
        'criteria': {
            'daily': ['aVWAP_avg', 'OB'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {
                          'direction': 'above',
                          'distance_pct': 1.0, 
                          'outside_range': True
                },
            },
            'OB': {
                'daily': {'mode': 'bearish'},
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
                '1hour': {'mode': 'resistance'}
            },
        }
    },

    'd_StDevOversold_4h_OBSupport': {
        'criteria': {
            'daily': ['StDev'],
            '4hour': ['OB']
        },
        'params': {
            'StDev': {
                'daily': {'mode': 'oversold', 'threshold': 1.5}
            },
            'OB': {
                '4hour': {'mode': 'support'}
            },
        }
    },

    'd_StDevOverbought_4h_OBResistance': {
        'criteria': {
            'daily': ['StDev'],
            '4hour': ['OB']
        },
        'params': {
            'StDev': {
                'daily': {'mode': 'overbought', 'threshold': 1.5}
            },
            'OB': {
                '4hour': {'mode': 'resistance'}
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
                'daily': {'mode': 'support'},
                '1hour': {'mode': 'support'}
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
                'daily': {'mode': 'resistance'},
                '1hour': {'mode': 'resistance'}
            },
        }
    },

    'd_OBSupport_4h_OBSupport': {
        'criteria': {
            'daily': ['OB'],
            '4hour': ['OB']
        },
        'params': {
            'OB': {
                'daily': {'mode': 'support'},
                '4hour': {'mode': 'support'}
            },
        }
    },

    'd_OBResistance_4h_OBResistance': {
        'criteria': {
            'daily': ['OB'],
            '4hour': ['OB']
        },
        'params': {
            'OB': {
                'daily': {'mode': 'resistance'},
                '4hour': {'mode': 'resistance'}
            },
        }
    },

    'd_OBBullish_h_OBBullish': {
        'criteria': {
            'daily': ['OB'],
            '1hour': ['OB']
        },
        'params': {
            'OB': {
                'daily': {'mode': 'bullish'},
                '1hour': {'mode': 'bullish'}
            },
        }
    },

    'd_OBBearish_h_OBBearish': {
        'criteria': {
            'daily': ['OB'],
            '1hour': ['OB']
        },
        'params': {
            'OB': {
                'daily': {'mode': 'bearish'},
                '1hour': {'mode': 'bearish'}
            },
        }
    },

    'd_OBSupport_4h_OBSupport': {
        'criteria': {
            'daily': ['OB'],
            '4hour': ['OB']
        },
        'params': {
            'OB': {
                'daily': {'mode': 'support'},
                '4hour': {'mode': 'support'}
            },
        }
    },

    'd_OBResistance_4h_OBResistance': {
        'criteria': {
            'daily': ['OB'],
            '4hour': ['OB']
        },
        'params': {
            'OB': {
                'daily': {'mode': 'resistance'},
                '4hour': {'mode': 'resistance'}
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
                'daily': {'mode': 'bullish', 'distance_pct': 1.0, 'direction': 'within'},
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

    'd_aVWAPPeaksavg_OBBullishaVWAP': {
        'criteria': {
            'daily': ['aVWAP_avg', 'OB_aVWAP'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {
                          'mode': 'peaks', 
                          'direction': 'within', 
                          'distance_pct': 0.5
                },
            },
            'OB_aVWAP': {
                'daily': {'mode': 'bullish', 'distance_pct': 1.0, 'direction': 'within'},
            },
        }
    },

    'd_aVWAPValleysavg_OBBearishaVWAP': {
        'criteria': {
            'daily': ['aVWAP_avg', 'OB_aVWAP'],
        },
        'params': {
            'aVWAP_avg': {
                'daily': {
                          'mode': 'valleys', 
                          'direction': 'within', 
                          'distance_pct': 0.5
                },
            },
            'OB_aVWAP': {
                'daily': {'mode': 'bearish', 'distance_pct': 1.0, 'direction': 'within'},
            },
        }
    },

    'd_StDevOversold_OBBullishaVWAP': {
        'criteria': {
            'daily': ['StDev', 'OB_aVWAP'],
        },
        'params': {
            'StDev': {
                'daily': {'mode': 'oversold', 'threshold': 1.5},
            },
            'OB_aVWAP': {
                'daily': {'mode': 'bullish', 'distance_pct': 1.0, 'direction': 'within'},
            },
        }
    },

    'd_StDevOverbought_OBBearishaVWAP': {
        'criteria': {
            'daily': ['StDev', 'OB_aVWAP'],
        },
        'params': {
            'StDev': {
                'daily': {'mode': 'overbought', 'threshold': 1.5},
            },
            'OB_aVWAP': {
                'daily': {'mode': 'bearish', 'distance_pct': 1.0, 'direction': 'within'},
            },
        }
    },

    'd_StDevOversold_OBBearishaVWAP': {
        'criteria': {
            'daily': ['StDev', 'OB_aVWAP'],
        },
        'params': {
            'StDev': {
                'daily': {'mode': 'oversold', 'threshold': 1.5},
            },
            'OB_aVWAP': {
                'daily': {'mode': 'bearish', 'distance_pct': 1.0, 'direction': 'within'},
            },
        }
    },

    'd_StDevOverbought_OBBullishaVWAP': {
        'criteria': {
            'daily': ['StDev', 'OB_aVWAP'],
        },
        'params': {
            'StDev': {
                'daily': {'mode': 'overbought', 'threshold': 1.5},
            },
            'OB_aVWAP': {
                'daily': {'mode': 'bullish', 'distance_pct': 1.0, 'direction': 'within'},
            },
        }
    },

    'd_OscVol': {
        'criteria': {
            'daily': ['oscillation_volatility'],
        },
        'params': {
            'oscillation_volatility': {
                'daily': {'cross_count': 1, 'avg_deviation': 0.0, 'oscillation_score': 3.0},
            }
        }
    },

    'd_OscVol_StDevOverbought': {
        'criteria': {
            'daily': ['oscillation_volatility', 'StDev'],
        },
        'params': {
            'oscillation_volatility': {
                'daily': {'cross_count': 1, 'avg_deviation': 0.0, 'oscillation_score': 2.0},
            },
            'StDev': {
                'daily': {'mode': 'overbought', 'threshold': 2}
            },
        }
    },

    'd_OscVol_StDevOversold': {
        'criteria': {
            'daily': ['oscillation_volatility', 'StDev'],
        },
        'params': {
            'oscillation_volatility': {
                'daily': {'cross_count': 1, 'avg_deviation': 0.0, 'oscillation_score': 2.0},
            },
            'StDev': {
                'daily': {'mode': 'oversold', 'threshold': 2}
            },
        }
    },

    'd_BoSBullish': {
        'criteria': {
            'daily': ['BoS_CHoCH'],
        },
        'params': {
            'BoS_CHoCH': {
                'daily': {'mode': 'BoS_bullish'},
            }
        }
    },

    'd_BoSBearish': {
        'criteria': {
            'daily': ['BoS_CHoCH'],
        },
        'params': {
            'BoS_CHoCH': {
                'daily': {'mode': 'BoS_bearish'},
            }
        }
    },

    'd_CHoCHBullish': {
        'criteria': {
            'daily': ['BoS_CHoCH'],
        },
        'params': {
            'BoS_CHoCH': {
                'daily': {'mode': 'CHoCH_bullish'},
            }
        }
    },

    'd_CHoCHBearish': {
        'criteria': {
            'daily': ['BoS_CHoCH'],
        },
        'params': {
            'BoS_CHoCH': {
                'daily': {'mode': 'CHoCH_bearish'},
            }
        }
    },

    'd_StDevOversold_h_CHoCHBullish': {
        'criteria': {
            'daily': ['StDev'],
            '1hour': ['BoS_CHoCH'],
        },
        'params': {
            'StDev': {
                'daily': {'mode': 'oversold'},
            },
            'BoS_CHoCH': {
                '1hour': {'mode': 'CHoCH_bullish'},
            }
        }
    },

    'd_StDevOverbought_h_CHoCHBearish': {
        'criteria': {
            'daily': ['StDev'],
            '1hour': ['BoS_CHoCH'],
        },
        'params': {
            'StDev': {
                'daily': {'mode': 'overbought'},
            },
            'BoS_CHoCH': {
                '1hour': {'mode': 'CHoCH_bearish'},
            }
        }
    },

    'd_aVWAPChannelBelow_OBBullish': {
        'criteria': {
            'daily': ['aVWAP_channel', 'OB_aVWAP'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {
                          'mode': 'support', 
                          'direction': 'below', 
                          'distance_pct': 0.1
                },
            },
            'OB': {
                'daily': {'mode': 'bullish'},
            },
        }
    },

    'd_aVWAPChannelAbove_OBBearish': {
        'criteria': {
            'daily': ['aVWAP_channel', 'OB'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {
                          'mode': 'resistance', 
                          'direction': 'above', 
                          'distance_pct': 0.1
                },
            },
            'OB': {
                'daily': {'mode': 'bearish'},
            },
        }
    },

    'd_aVWAPChannelBelow_OBBullishaVWAP': {
        'criteria': {
            'daily': ['aVWAP_channel', 'OB_aVWAP'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {
                          'mode': 'support', 
                          'direction': 'below', 
                          'distance_pct': 0.1
                },
            },
            'OB_aVWAP': {
                'daily': {'mode': 'bullish', 'distance_pct': 0.1, 'direction': 'above'},
            },
        }
    },

    'd_aVWAPChannelAbove_OBBearishaVWAP': {
        'criteria': {
            'daily': ['aVWAP_channel', 'OB_aVWAP'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {
                          'mode': 'resistance', 
                          'direction': 'above', 
                          'distance_pct': 0.1
                },
            },
            'OB_aVWAP': {
                'daily': {'mode': 'bearish', 'distance_pct': 0.1, 'direction': 'below'},
            },
        }
    },

    'd_aVWAPChannelBelow': {
        'criteria': {
            'daily': ['aVWAP_channel'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {
                          'mode': 'support', 
                          'direction': 'below', 
                          'distance_pct': 1.0
                },
            },
        }
    },

    'd_aVWAPChannelAbove': {
        'criteria': {
            'daily': ['aVWAP_channel'],
        },
        'params': {
            'aVWAP_channel': {
                'daily': {
                          'mode': 'resistance', 
                          'direction': 'above', 
                          'distance_pct': 1.0
                },
            },
        }
    },

}
