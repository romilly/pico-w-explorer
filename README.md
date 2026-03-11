# pico-w-explorer

Code for the Pimoroni Pico W Explorer board.

## Focus Reminder

A daily focus reminder that flashes the onboard LED and beeps the buzzer at configured times. Supports multiple independently-dismissible alerts per day. Press Button A to dismiss the current alert, or it auto-dismisses after 10 seconds. Each alert resets automatically the next day. Alerts that are already past when the device powers on are silently skipped.

Currently configured for reminders at 12:45, 14:00 and 16:00 UTC.

The display shows:
- **Top line**: weekday name with a live clock (HH:MM, updates each minute)
- **Reminders label** in blue
- **Reminder times** in red

Built using hexagonal architecture with ports and adapters, developed test-first with TDD.

## Project Structure

```
src/pico_w_explorer/
    ports/              # Port interfaces (clock, buzzer, led, button, display)
    adapters/           # Real Pico W hardware adapters
    application.py      # ApplicationConfig and Application (wiring and run loop)
    colour.py           # Colour class with RGB values and constants
    text_spec.py        # TextSpec class (font, colour, thickness, scale)
    focus_reminder.py   # Domain logic (AlertState, FocusReminder)
    widgets.py          # Text widget with clearing and TextSpec support
    main.py             # Entry point for the Pico
tests/
    adapters/           # Fake adapters for testing
    builders.py         # ApplicationBuilder for test setup
    matchers.py         # Custom PyHamcrest matchers (rect, rect_list)
    test_application.py
    test_colour.py
    test_focus_reminder.py
    test_text_spec.py
    test_widgets.py
    test_walking_skeleton.py
docs/
    tick-driven-testing.md  # Integration testing pattern
plan/
    progress-2026-03-11.md  # Latest progress report
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
# Set up virtual environment (activated automatically by Claude Code hook)
pip install -r requirements-test.txt

# Run tests
pytest

# Type check domain code
pyright src/pico_w_explorer/ports/ src/pico_w_explorer/focus_reminder.py src/pico_w_explorer/application.py src/pico_w_explorer/colour.py src/pico_w_explorer/text_spec.py src/pico_w_explorer/widgets.py
```
