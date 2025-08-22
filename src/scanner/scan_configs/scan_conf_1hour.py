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
            '1hour': ['aVWAP_channel'],
        },
        'params': {
            'aVWAP_channel': {
                '1hour': {'mode': 'resistance', 'distance_pct': 1.0}
            },
        }
    },

    'h_aVWAPChannelSupport': {
        'criteria': {
            '1hour': ['aVWAP_channel'],
        },
        'params': {
            'aVWAP_channel': {
                '1hour': {'mode': 'support', 'distance_pct': 5.0}
            },
        }
    },

    'h_aVWAPChannelSupport_OBSupport': {
        'criteria': {
            '1hour': ['aVWAP_channel', 'OB'],
        },
        'params': {
            'aVWAP_channel': {
                '1hour': {'mode': 'support', 'distance_pct': 5.0}
            },
            'OB': {
                '1hour': {'mode': 'support'}
            },
        }
    },

    'h_aVWAPPeaksavg': {
        'criteria': {
            '1hour': ['aVWAP_avg'],
        },
        'params': {
            'aVWAP_avg': {
                '1hour': {'mode': 'peaks', 'distance_pct': 1.0}
            },
        }
    },

    'h_aVWAPValleysavg': {
        'criteria': {
            '1hour': ['aVWAP_avg'],
        },
        'params': {
            'aVWAP_avg': {
                '1hour': {'mode': 'valleys', 'distance_pct': 1.0}
            },
        }
    },

    'h_StDevOversold_OBSupport': {
        'criteria': {
            '1hour': ['StDev', 'OB'],
        },
        'params': {
            'StDev': {
                '1hour': {'threshold': 2, 'mode': 'oversold'}
            },
            'OB': {
                '1hour': {'mode': 'support'}
            },
        }
    },

    'h_StDevOverbought_OBResistance': {
        'criteria': {
            '1hour': ['StDev', 'OB'],
        },
        'params': {
            'StDev': {
                '1hour': {'threshold': 2, 'mode': 'overbought'}
            },
            'OB': {
                '1hour': {'mode': 'resistance'}
            },
        }
    },

    'h_StDevOversold_OBBullish': {
        'criteria': {
            '1hour': ['StDev', 'OB'],
        },
        'params': {
            'StDev': {
                '1hour': {'threshold': 2, 'mode': 'oversold'}
            },
            'OB': {
                '1hour': {'mode': 'bullish'}
            },
        }
    },

    'h_StDevOverbought_OBBearish': {
        'criteria': {
            '1hour': ['StDev', 'OB'],
        },
        'params': {
            'StDev': {
                '1hour': {'threshold': 2, 'mode': 'overbought'}
            },
            'OB': {
                '1hour': {'mode': 'bearish'}
            },
        }
    },

    'h_OBSupport': {
        'criteria': {
            '1hour': ['OB'],
        },
        'params': {
            'OB': {
                '1hour': {'mode': 'support'}
            },
        }
    },

    'h_OBResistance': {
        'criteria': {
            '1hour': ['OB'],
        },
        'params': {
            'OB': {
                '1hour': {'mode': 'resistance'}
            },
        }
    },

    'h_supertrendBullish_QQEMODOversold': {
        'criteria': {
            '1hour': ['supertrend', 'QQEMOD'],
        },
        'params': {
            'supertrend': {
                '1hour': {'mode': 'bullish'},
            }
        },
        'QQEMOD': {
            '1hour': {'mode': 'oversold'},
        }
    },

    'h_bankerRSI_QQEMODOversold': {
        'criteria': {
            '1hour': ['banker_RSI', 'QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                '1hour': {'mode': 'oversold'},
            }
        }
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
            '1hour': ['SMA'],
        },
        'params': {
            'SMA': {
                '1hour': {'sma_periods': [200], 'distance_pct': 1.0, 'outside_range': False},
            }
        }
    },

    'h_SMABelow': {
        'criteria': {
            '1hour': ['SMA'],
        },
        'params': {
            'SMA': {
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
            '1hour': ['QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                '1hour': {'mode': 'bullish_reversal'},
            }
        }
    },

    'h_QQEMODBearishReversal': {
        'criteria': {
            '1hour': ['QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                '1hour': {'mode': 'bearish_reversal'},
            }
        }
    },

    'h_aVWAPavgBelow_OBBullish': {
        'criteria': {
            '1hour': ['aVWAP_avg', 'OB'],
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
            }
        }
    },

    'h_OscVol': {
        'criteria': {
            '1hour': ['oscillation_volatility'],
        },
        'params': {
            'oscillation_volatility': {
                '1hour': {'cross_count': 1, 'avg_deviation': 0.0, 'oscillation_score': 3.0},
            }
        }
    },

    'h_CHoCHBullish': {
        'criteria': {
            '1hour': ['BoS_CHoCH'],
        },
        'params': {
            'BoS_CHoCH': {
                '1hour': {'mode': 'CHoCH_bullish'},
            }
        }
    },

    'h_aVWAPChannelSupport_aVWAPPeaksavg': {
        'criteria': {
            '1hour': ['aVWAP_channel', 'aVWAP_avg'],
        },
        'params': {
            'aVWAP_channel': {
                '1hour': {'mode': 'support', 'direction': 'within', 'distance_pct': 1.0}
            },
            'aVWAP_avg': {
                '1hour': {
                          'mode': 'peaks', 
                          'direction': 'within', 
                          'distance_pct': 0.5, 
                         }
            },
        }
    },

    'h_aVWAPChannelSupport_aVWAPValleysavg': {
        'criteria': {
            '1hour': ['aVWAP_channel', 'aVWAP_avg'],
        },
        'params': {
            'aVWAP_channel': {
                '1hour': {'mode': 'support', 'direction': 'within', 'distance_pct': 1.0}
            },
            'aVWAP_avg': {
                '1hour': {
                          'mode': 'valleys', 
                          'direction': 'within', 
                          'distance_pct': 0.5, 
                         }
            },
        }
    },

    'h_aVWAPChannelResistance_aVWAPValleysavg': {
        'criteria': {
            '1hour': ['aVWAP_channel', 'aVWAP_avg'],
        },
        'params': {
            'aVWAP_channel': {
                '1hour': {'mode': 'resistance', 'direction': 'within', 'distance_pct': 1.0}
            },
            'aVWAP_avg': {
                '1hour': {
                          'mode': 'valleys', 
                          'direction': 'within', 
                          'distance_pct': 1.0, 
                         }
            },
        }
    },

    'h_aVWAPChannelResistance_aVWAPPeaksavg': {
        'criteria': {
            '1hour': ['aVWAP_channel', 'aVWAP_avg'],
        },
        'params': {
            'aVWAP_channel': {
                '1hour': {'mode': 'resistance', 'direction': 'within', 'distance_pct': 1.0}
            },
            'aVWAP_avg': {
                '1hour': {
                          'mode': 'peaks', 
                          'direction': 'within', 
                          'distance_pct': 0.5, 
                         }
            },
        }
    },

    'h_aVWAPChannelBelow_OBBullishaVWAP': {
        'criteria': {
            '1hour': ['aVWAP_channel', 'OB_aVWAP'],
        },
        'params': {
            'aVWAP_channel': {
                '1hour': {
                          'mode': 'support', 
                          'direction': 'below', 
                          'distance_pct': 0.5
                },
            },
            'OB_aVWAP': {
                '1hour': {'mode': 'bullish', 'distance_pct': None, 'direction': 'above'},
            },
        }
    },

    'h_aVWAPChannelAbove_OBBearishaVWAP': {
        'criteria': {
            '1hour': ['aVWAP_channel', 'OB_aVWAP'],
        },
        'params': {
            'aVWAP_channel': {
                '1hour': {
                          'mode': 'resistance', 
                          'direction': 'above', 
                          'distance_pct': 0.5
                },
            },
            'OB_aVWAP': {
                '1hour': {'mode': 'bearish', 'distance_pct': None, 'direction': 'below'},
            },
        }
    },

}
