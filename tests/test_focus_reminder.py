import pytest

from pico_w_explorer.focus_reminder import FocusReminder
from tests.adapters.fake_buzzer import FakeBuzzer
from tests.adapters.fake_button import FakeButton
from tests.adapters.fake_clock import FakeClock
from tests.adapters.fake_led import FakeLed


class ReminderFixture:
    def __init__(self) -> None:
        self.clock = FakeClock()
        self.buzzer = FakeBuzzer()
        self.led = FakeLed()
        self.button = FakeButton()

    def create(self, reminder_hour: int = 14, reminder_minute: int = 0) -> FocusReminder:
        return FocusReminder(
            self.clock, self.buzzer, self.led, self.button,
            reminder_hour=reminder_hour, reminder_minute=reminder_minute,
        )


@pytest.fixture
def fix() -> ReminderFixture:
    return ReminderFixture()


def test_no_alert_before_reminder_time(fix: ReminderFixture) -> None:
    fix.clock.set_time(13, 0)
    reminder = fix.create()

    reminder.tick()

    assert fix.buzzer.on is False
    assert fix.led.on is False


def test_alert_starts_at_reminder_time(fix: ReminderFixture) -> None:
    fix.clock.set_time(14, 0)
    reminder = fix.create()

    reminder.tick()

    assert fix.buzzer.on is True
    assert fix.led.on is True


def test_alert_continues_past_reminder_time(fix: ReminderFixture) -> None:
    fix.clock.set_time(14, 5)
    reminder = fix.create()

    reminder.tick()

    assert fix.buzzer.on is True
    assert fix.led.on is True


def test_button_press_dismisses_alert(fix: ReminderFixture) -> None:
    fix.clock.set_time(14, 0)
    reminder = fix.create()

    reminder.tick()  # starts alerting
    fix.button.press()
    reminder.tick()  # should dismiss

    assert fix.buzzer.on is False
    assert fix.led.on is False


def test_alert_stays_dismissed_after_button_release(fix: ReminderFixture) -> None:
    fix.clock.set_time(14, 0)
    reminder = fix.create()

    reminder.tick()  # starts alerting
    fix.button.press()
    reminder.tick()  # dismisses
    fix.button.release()
    reminder.tick()  # should stay silent

    assert fix.buzzer.on is False
    assert fix.led.on is False


def test_dismissed_resets_next_day(fix: ReminderFixture) -> None:
    fix.clock.set_time(14, 0)
    reminder = fix.create()

    reminder.tick()  # starts alerting
    fix.button.press()
    reminder.tick()  # dismisses
    fix.button.release()

    # Next day, before reminder time — still silent
    fix.clock.set_day(2)
    fix.clock.set_time(13, 0)
    reminder.tick()
    assert fix.buzzer.on is False
    assert fix.led.on is False

    # Next day, at reminder time — alert fires again
    fix.clock.set_time(14, 0)
    reminder.tick()
    assert fix.buzzer.on is True
    assert fix.led.on is True
