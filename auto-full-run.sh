#!/bin/bash

cd /home/mjc/Desktop/Dev/tiingo-screener-python

source venv/bin/activate

touch "script_run_$(date +'%Y-%m-%d_%H-%M-%S').log"

echo "DELETE" | python app.py --full-run

toucn "script_run_FINAL_$(date +'%Y-%m-%d_%H-%M-%S').log"

git add .
git commit -m "Auto-commit: Daily tickers/indicators for $(date +'%Y-%m-%d')"
git push
