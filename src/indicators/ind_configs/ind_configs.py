import importlib
from pathlib import Path
from typing import Dict, Any

# Initialize combined dictionaries
all_indicators = {}
all_params = {}

# Load and merge all config files
for f in Path(__file__).parent.glob('ind_conf_*.py'):
    config_id = f.stem.split('_')[-1]  # Extract the number
    module = importlib.import_module(f".{f.stem}", package=__package__)
    
    # For all configs, create both numbered and unnumbered versions for config 1
    for timeframe, ind_list in module.indicators.items():
        if config_id == '1':
            # Add both 'daily' and 'daily_1' pointing to same config
            all_indicators[timeframe] = ind_list
            all_indicators[f"{timeframe}_1"] = ind_list
        else:
            all_indicators[f"{timeframe}_{config_id}"] = ind_list
    
    for timeframe, param_set in module.params.items():
        if config_id == '1':
            # Add both 'daily' and 'daily_1' pointing to same config
            all_params[timeframe] = param_set
            all_params[f"{timeframe}_1"] = param_set
        else:
            all_params[f"{timeframe}_{config_id}"] = param_set

# Export the combined dictionaries
indicators = all_indicators
params = all_params
