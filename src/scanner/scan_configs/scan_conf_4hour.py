scan_conf = {

    # 4hour ==============================================

    '4h_aVWAPChannelOverbought': {
        'criteria': {
            '4hour': ['aVWAP_channel_resistance'],
        },
        'params': {
            'aVWAP_channel_resistance': {
                '4hour': {'distance_pct': 10.0, 'direction': 'above'}
            },
        }
    },

    '4h_aVWAPChannelOversold': {
        'criteria': {
            '4hour': ['aVWAP_channel_support'],
        },
        'params': {
            'aVWAP_channel_support': {
                '4hour': {'distance_pct': 10.0, 'direction': 'below'}
            },
        }
    },

    '4h_aVWAPChannelResistance': {
        'criteria': {
            '4hour': ['aVWAP_channel_resistance'],
        },
        'params': {
            'aVWAP_channel_resistance': {
                '4hour': {'distance_pct': 5.0, 'direction': 'within'}
            },
        }
    },

    '4h_aVWAPChannelSupport': {
        'criteria': {
            '4hour': ['aVWAP_channel_support'],
        },
        'params': {
            'aVWAP_channel_support': {
                '4hour': {'distance_pct': 5.0, 'direction': 'within'}
            },
        }
    },

    '4h_aVWAPPeaksavg': {
        'criteria': {
            '4hour': ['aVWAP_peaks_avg'],
        },
        'params': {
            'aVWAP_peaks_avg': {
                '4hour': {'distance_pct': 1.0, 'direction': 'within'}
            },
        }
    },

    '4h_aVWAPValleysavg': {
        'criteria': {
            '4hour': ['aVWAP_valleys_avg'],
        },
        'params': {
            'aVWAP_valleys_avg': {
                '4hour': {'distance_pct': 1.0, 'direction': 'within'}
            },
        }
    },

    '4h_StDevOversold_OBSupport': {
        'criteria': {
            '4hour': ['StDev', 'OB'],
        },
        'params': {
            'StDev': {
                '4hour': {'threshold': 2, 'mode': 'oversold'}
            },
            'OB': {
                '4hour': {'mode': 'support'}
            },
        }
    },

    '4h_OBSupport': {
        'criteria': {
            '4hour': ['OB'],
        },
        'params': {
            'OB': {
                '4hour': {'mode': 'support'}
            },
        }
    },

    '4h_supertrendBullish_QQEMODOversold': {
        'criteria': {
            '4hour': ['supertrend', 'QQEMOD'],
        },
        'params': {
            'supertrend': {
                '4hour': {'mode': 'bullish'},
            },
            'QQEMOD': {
                '4hour': {'mode': 'oversold'},
            },
        }
    },

    '4h_bankerRSI_QQEMODOversold': {
        'criteria': {
            '4hour': ['banker_RSI', 'QQEMOD_oversold'],
        },
        'params': {
            'QQEMOD': {
                '4hour': {'mode': 'oversold'},
            }
        }
    },

    '4h_SMA': {
        'criteria': {
            '4hour': ['SMA'],
        },
        'params': {
            'SMA': {
                '4hour': {'sma_periods': [50], 'distance_pct': 1.0},
            }
        }
    },

    '4h_SMAAbove': {
        'criteria': {
            '4hour': ['SMA'],
        },
        'params': {
            'SMA': {
                '4hour': {'sma_periods': [200], 'distance_pct': 1.0, 'outside_range': False},
            }
        }
    },

    '4h_SMABelow': {
        'criteria': {
            '4hour': ['SMA'],
        },
        'params': {
            'SMA': {
                '4hour': {'sma_periods': [200], 'distance_pct': 1.0, 'outside_range': False},
            }
        }
    },

    '4h_TTMSqueeze': {
        'criteria': {
            '4hour': ['TTM_squeeze'],
        },
        'params': {
            'TTM_squeeze': {
                '4hour': {'min_squeeze_bars': 5, 'max_squeeze_bars': None},
            }
        }
    },

    '4h_QQEMODBullishReversal': {
        'criteria': {
            '4hour': ['QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                '4hour': {'mode': 'bullish_reversal'},
            }
        }
    },

    '4h_QQEMODBearishReversal': {
        'criteria': {
            '4hour': ['QQEMOD'],
        },
        'params': {
            'QQEMOD': {
                '4hour': {'mode': 'bearish_reversal'},
            }
        }
    },

    '4h_aVWAPavgBelow_OBBullish': {
        'criteria': {
            '4hour': ['aVWAP_avg', 'OB'],
        },
        'params': {
            'aVWAP_avg': {
                '4hour': {
                          'direction': 'below',
                          'distance_pct': 1.0, 
                          'outside_range': False
                },
            },
            'OB': {
                '4hour': {'mode': 'bullish'},
            }
        }
    },

}

