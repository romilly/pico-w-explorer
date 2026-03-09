#!/bin/bash
# Deploy focus reminder to Pico W Explorer
# Usage: ./deploy.sh

set -e

# Remove __pycache__ dirs before deploying
find src/pico_w_explorer -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

echo "Cleaning Pico filesystem..."
mpremote rm -r :pico_w_explorer 2>/dev/null || true
mpremote rm :main.py 2>/dev/null || true
mpremote rm :WIFI_CONFIG.py 2>/dev/null || true

echo "Deploying pico_w_explorer to Pico W..."
mpremote \
    mkdir :pico_w_explorer + \
    mkdir :pico_w_explorer/ports + \
    mkdir :pico_w_explorer/adapters + \
    cp src/pico_w_explorer/__init__.py :pico_w_explorer/__init__.py + \
    cp src/pico_w_explorer/application.py :pico_w_explorer/application.py + \
    cp src/pico_w_explorer/colour.py :pico_w_explorer/colour.py + \
    cp src/pico_w_explorer/widgets.py :pico_w_explorer/widgets.py + \
    cp src/pico_w_explorer/focus_reminder.py :pico_w_explorer/focus_reminder.py + \
    cp src/pico_w_explorer/ports/*.py :pico_w_explorer/ports/ + \
    cp src/pico_w_explorer/adapters/*.py :pico_w_explorer/adapters/ + \
    cp src/pico_w_explorer/main.py :main.py + \
    cp src/pico_w_explorer/WIFI_CONFIG.py :WIFI_CONFIG.py + \
    reset
echo "Deployed. Device will restart and run main.py."
