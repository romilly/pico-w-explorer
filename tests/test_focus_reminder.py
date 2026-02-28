from pico_w_explorer.focus_reminder import FocusReminder
from tests.fakes import FakeBuzzer, FakeButton, FakeClock, FakeLed


def test_no_alert_before_reminder_time() -> None:
    clock = FakeClock(hour=13, minute=0)
    buzzer = FakeBuzzer()
    led = FakeLed()
    button = FakeButton()
    reminder = FocusReminder(clock, buzzer, led, button, reminder_hour=14, reminder_minute=0)

    reminder.tick()

    assert buzzer.on is False
    assert led.on is False


def test_alert_starts_at_reminder_time() -> None:
    clock = FakeClock(hour=14, minute=0)
    buzzer = FakeBuzzer()
    led = FakeLed()
    button = FakeButton()
    reminder = FocusReminder(clock, buzzer, led, button, reminder_hour=14, reminder_minute=0)

    reminder.tick()

    assert buzzer.on is True
    assert led.on is True
