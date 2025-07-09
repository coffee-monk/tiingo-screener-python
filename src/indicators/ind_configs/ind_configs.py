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
    
    # For first config, use base names
    if config_id == '1':
        all_indicators.update(module.indicators)
        all_params.update(module.params)
    # For subsequent configs, add numbered variants
    else:
        for timeframe, ind_list in module.indicators.items():
            all_indicators[f"{timeframe}_{config_id}"] = ind_list
        for timeframe, param_set in module.params.items():
            all_params[f"{timeframe}_{config_id}"] = param_set

# Export the combined dictionaries
indicators = all_indicators
params = all_params
