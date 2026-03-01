# pico-w-explorer

Code for the Pimoroni Pico W Explorer board.

## Focus Reminder

A daily focus reminder that flashes the onboard LED and beeps the buzzer at configured times. Supports multiple independently-dismissible alerts per day. Press Button A to dismiss the current alert. Each alert resets automatically the next day.

Currently configured for reminders at 12:45 and 16:00 UTC.

Built using hexagonal architecture with ports and adapters, developed test-first with TDD.

## Project Structure

```
src/pico_w_explorer/
    ports/              # Port interfaces (clock, buzzer, led, button, display)
    adapters/           # Real Pico W hardware adapters
    application.py      # Application wiring and run loop
    focus_reminder.py   # Domain logic (AlertState, FocusReminder)
    main.py             # Entry point for the Pico
tests/
    adapters/           # Fake adapters for testing
    builders.py         # ApplicationBuilder for test setup
    test_focus_reminder.py
    test_walking_skeleton.py
docs/
    tick-driven-testing.md  # Integration testing pattern
```

## Deployment

Requires [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) and a Pico W connected via USB.

```bash
./deploy.sh
```

This copies the package to the Pico and restarts it. The device connects to WiFi, syncs the clock via NTP, and runs the reminder loop.

## WiFi Configuration

Copy the example config and fill in your credentials:

```bash
cp src/pico_w_explorer/WIFI_CONFIG.py.example src/pico_w_explorer/WIFI_CONFIG.py
```

## Development

```bash
# Set up virtual environment
source venv/bin/activate
pip install -r requirements-test.txt

# Run tests
pytest

# Type check domain code
pyright src/pico_w_explorer/ports/ src/pico_w_explorer/focus_reminder.py src/pico_w_explorer/application.py
```
