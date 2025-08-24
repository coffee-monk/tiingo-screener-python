#!/bin/bash

# Navigate to your project directory
cd /home/mjc/Desktop/Dev/tiingo-screener-python

# Activate virtual environment
source venv/bin/activate

# Run your Python application and automatically respond "DELETE" when prompted
echo "DELETE" | python app.py --full-run

# Git operations
git add .
git commit -m "Auto-commit: Daily tickers/indicators for $(date +'%Y-%m-%d')"
git push
