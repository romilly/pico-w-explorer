# pico-w-explorer

Code for the Pimoroni Pico W Explorer board.

## Focus Reminder

A daily focus reminder that flashes the onboard LED and beeps the speaker at a configured time (default 16:00 UTC). Press Button A to dismiss. The alert resets automatically the next day.

Built using hexagonal architecture with ports and adapters, developed test-first with TDD.

## Project Structure

```
src/pico_w_explorer/
    ports/          # Port interfaces (clock, buzzer, led, button)
    adapters/       # Real Pico W hardware adapters
    focus_reminder.py   # Domain logic
    main.py         # Entry point for the Pico
tests/
    adapters/       # Fake adapters for testing
    test_focus_reminder.py
    test_walking_skeleton.py
```

## Deployment

Requires [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) and a Pico W connected via USB.

```bash
./deploy.sh
```

This copies the package to the Pico and restarts it. The device connects to WiFi, syncs the clock via NTP, and runs the reminder loop.

## Development

```bash
# Set up virtual environment
source venv/bin/activate
pip install -r requirements-test.txt

# Run tests
pytest

# Type check domain code
pyright src/pico_w_explorer/ports/ src/pico_w_explorer/focus_reminder.py
```
