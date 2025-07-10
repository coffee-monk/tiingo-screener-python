import importlib
from pathlib import Path

scan_configs = {}

# Dynamically load all scan_conf_*.py files
for config_file in Path(__file__).parent.glob('scan_conf_*.py'):
    try:
        module = importlib.import_module(f'.{config_file.stem}', package=__package__)
        scan_configs.update(module.scan_conf)
    except Exception as e:
        print(f"Error loading {config_file.stem}: {e}")
        continue

scan_configs = scan_configs
