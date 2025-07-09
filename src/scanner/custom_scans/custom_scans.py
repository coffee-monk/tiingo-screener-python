from .scans_weekly import scans_weekly
from .scans_daily import scans_daily
from .scans_1hour import scans_1hour
from .scans_5min import scans_5min

# Combine all scan configurations
custom_scans = {}
custom_scans.update(scans_weekly)
custom_scans.update(scans_daily)
custom_scans.update(scans_1hour)
custom_scans.update(scans_5min)
