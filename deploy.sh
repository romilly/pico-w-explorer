#!/bin/bash
# Deploy focus reminder to Pico W Explorer
# Usage: ./deploy.sh

set -e

# Remove __pycache__ dirs before deploying
find src/pico_w_explorer -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

echo "Deploying pico_w_explorer to Pico W..."
mpremote \
    cp -r src/pico_w_explorer/ :pico_w_explorer/ + \
    cp src/pico_w_explorer/main.py :main.py + \
    soft-reset
echo "Deployed. Device will restart and run main.py."
