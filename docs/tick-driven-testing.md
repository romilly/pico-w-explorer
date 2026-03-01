# Tick-Driven Integration Testing Pattern

## Problem

Integration tests that reach into builder internals to manipulate fakes are a code smell:

```python
# BAD — test reaches into builder to jump time and check state
builder.clock.set_time(14, 0)
app.tick()
assert builder.buzzer.on is True
```

This exposes implementation details and makes tests fragile.

## The Pattern

Inspired by [tdd-lazydoro](~/git/active/tdd-lazydoro), integration tests should:

1. **Create fakes outside the builder** — test owns them, not the builder
2. **Inject fakes via `with_xxx()` methods** — explicit dependency injection
3. **Drive time through ticks** — not by setting clocks
4. **Use helper methods** — so the test reads like a story
5. **Use `build_app()` for per-test configuration** — different tests can use different reminder times

### Architecture

```
Test creates fakes → injects into Builder via with_xxx() → Builder creates Application
Test holds refs to fakes ↗                                              ↓
Test calls app.tick() ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←↙
```

### Tick-Driven FakeClock

The FakeClock supports two modes:
- **`set_time(h, m)`** — for unit tests where jumping to a specific time is appropriate
- **`tick()`** — for integration tests where time flows naturally

```python
class FakeClock(ClockPort):
    def __init__(self, hour: int = 0, minute: int = 0, day: int = 1) -> None:
        self._hour = hour
        self._minute = minute
        self._day = day

    def tick(self) -> None:
        """Advance clock by one minute."""
        self._minute += 1
        if self._minute >= 60:
            self._minute = 0
            self._hour += 1
            if self._hour >= 24:
                self._hour = 0
                self._day += 1

    def current_time(self) -> tuple[int, int]:
        return (self._hour, self._minute)

    def current_date(self) -> int:
        return self._day
```

### Integration Test Structure

```python
class TestFullApplicationLifecycle:
    def setup_method(self) -> None:
        # Test creates and owns the fakes
        self.clock = FakeClock()
        self.buzzer = FakeBuzzer()
        self.led = FakeLed()
        self.button = FakeButton()

    def build_app(self, start_hour: int = 13, start_minute: int = 0,
                  reminder_times: list[tuple[int, int]] | None = None) -> None:
        # Inject fakes via with_xxx() — don't read them back from builder
        builder = (
            ApplicationBuilder()
            .with_clock(self.clock)
            .with_buzzer(self.buzzer)
            .with_led(self.led)
            .with_button(self.button)
            .with_time(start_hour, start_minute)
        )
        if reminder_times is not None:
            builder = builder.with_reminder_times(reminder_times)
        self.app = builder.build()
        self.app.start()

    # --- Helper methods (read like a story) ---

    def wait(self, minutes: int = 1) -> None:
        for _ in range(minutes):
            self.clock.tick()
            self.app.tick()

    def press_button(self) -> None:
        self.button.press()

    def release_button(self) -> None:
        self.button.release()

    def assert_alerting(self) -> None:
        assert self.buzzer.on is True
        assert self.led.on is True

    def assert_silent(self) -> None:
        assert self.buzzer.on is False
        assert self.led.on is False

    # --- Single alert test ---

    def test_single_alert_lifecycle(self) -> None:
        self.build_app()

        self.wait(minutes=30)
        self.assert_silent()

        self.wait(minutes=30)  # reaches 14:00
        self.assert_alerting()

        self.press_button()
        self.wait()
        self.assert_silent()

        self.release_button()
        self.wait()
        self.assert_silent()

    # --- Multi-alert test ---

    def test_multiple_alerts_lifecycle(self) -> None:
        self.build_app(reminder_times=[(14, 0), (15, 0)])

        self.wait(minutes=30)
        self.assert_silent()

        # First alert at 14:00
        self.wait(minutes=30)
        self.assert_alerting()

        self.press_button()
        self.wait()
        self.assert_silent()
        self.release_button()

        # Still silent before second alert
        self.wait(minutes=29)
        self.assert_silent()

        # Second alert at 15:00
        self.wait(minutes=30)
        self.assert_alerting()

        self.press_button()
        self.wait()
        self.assert_silent()
```

### Compare: lazydoro's Walking Skeleton

The same pattern in lazydoro (the reference implementation):

```python
class AlmostE2ETestCase(unittest.TestCase):
    def setUp(self):
        self.rangefinder = MockRangeFinder()
        self.display = MockDisplay()
        self.watcher = build(rangefinder=self.rangefinder,
                             display=self.display, speed=100)

    def test_tracks_full_pomodoro(self):
        self.person_absent()
        self.wait(1)
        self.check_leds_are_off()
        self.person_present()
        self.wait(seconds=10)
        assert_that(self.display, shows_only(BLUE))
        # ...

    def wait(self, minutes=0, seconds=0):
        for i in range(seconds + minutes * self.ticks_per_minute):
            self.watcher.tick()

    def person_present(self):
        self.rangefinder.person_present()
```

## Key Principles

| Principle | Example |
|-----------|---------|
| **Test creates and owns fakes** | `self.clock = FakeClock()` in setup, injected via `with_clock()` |
| **Builder only used for construction** | After `build()`, never reference the builder again |
| **Time flows through ticks** | `self.wait(minutes=30)` not `clock.set_time(14, 0)` |
| **Helper methods tell a story** | `self.press_button()` not `self.button.press()` |
| **`build_app()` for per-test config** | Different tests can use different reminder times |
| **Unit tests can still jump** | `set_time()` is fine for focused unit tests of domain logic |

## When to Apply

- **Integration / walking skeleton tests** — always use tick-driven helpers with external fakes
- **Unit tests** — jumping to specific states with `set_time()` is fine; these test focused behaviour, not the flow of time
