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

    def create(self, reminder_times: list[tuple[int, int]] | None = None) -> FocusReminder:
        if reminder_times is None:
            reminder_times = [(14, 0)]
        return FocusReminder(
            self.clock, self.buzzer, self.led, self.button,
            reminder_times=reminder_times,
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
    fix.clock.set_time(13, 0)
    reminder = fix.create()
    fix.clock.set_time(14, 0)

    reminder.tick()

    assert fix.buzzer.on is True
    assert fix.led.on is True


def test_alert_continues_past_reminder_time(fix: ReminderFixture) -> None:
    fix.clock.set_time(13, 0)
    reminder = fix.create()
    fix.clock.set_time(14, 5)

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


def test_second_alert_fires_after_first_dismissed(fix: ReminderFixture) -> None:
    fix.clock.set_time(13, 0)
    reminder = fix.create(reminder_times=[(14, 0), (16, 0)])
    fix.clock.set_time(14, 0)

    reminder.tick()           # 14:00 alert is active and alerting
    fix.button.press()
    reminder.tick()           # 14:00 alert dismissed
    fix.button.release()

    # Advance to 16:00 — second alert fires
    fix.clock.set_time(16, 0)
    reminder.tick()
    assert fix.buzzer.on is True
    assert fix.led.on is True


def test_only_earliest_alert_fires_when_both_due(fix: ReminderFixture) -> None:
    fix.clock.set_time(13, 0)
    reminder = fix.create(reminder_times=[(14, 0), (16, 0)])
    fix.clock.set_time(16, 0)

    reminder.tick()  # first tick — only 14:00 alert should be active
    assert fix.buzzer.on is True

    # Dismiss 14:00 alert
    fix.button.press()
    reminder.tick()
    fix.button.release()

    # 16:00 takes over
    reminder.tick()
    assert fix.buzzer.on is True
    assert fix.led.on is True


def test_second_alert_fires_at_its_own_time(fix: ReminderFixture) -> None:
    fix.clock.set_time(15, 0)  # only 14:00 is due, not 16:00
    reminder = fix.create(reminder_times=[(14, 0), (16, 0)])

    reminder.tick()
    fix.button.press()
    reminder.tick()   # dismiss 14:00 alert
    fix.button.release()

    # 15:00 — 16:00 not yet due, should be silent
    reminder.tick()
    assert fix.buzzer.on is False
    assert fix.led.on is False

    # Advance to 16:00
    fix.clock.set_time(16, 0)
    reminder.tick()
    assert fix.buzzer.on is True
    assert fix.led.on is True


def test_each_alert_resets_independently_next_day(fix: ReminderFixture) -> None:
    fix.clock.set_time(16, 0)
    reminder = fix.create(reminder_times=[(14, 0), (16, 0)])

    # Dismiss both alerts today
    reminder.tick()           # 14:00 alerts
    fix.button.press()
    reminder.tick()           # dismiss 14:00
    fix.button.release()
    reminder.tick()           # 16:00 alerts
    fix.button.press()
    reminder.tick()           # dismiss 16:00
    fix.button.release()

    # Both dismissed — silent
    reminder.tick()
    assert fix.buzzer.on is False

    # Next day — both alerts reset
    fix.clock.set_day(2)
    fix.clock.set_time(16, 0)
    reminder.tick()
    assert fix.buzzer.on is True
    assert fix.led.on is True


def test_no_alert_if_powered_on_after_reminder_time(fix: ReminderFixture) -> None:
    fix.clock.set_time(15, 0)  # powered on an hour after 14:00 reminder
    reminder = fix.create()

    reminder.tick()

    assert fix.buzzer.on is False
    assert fix.led.on is False


def test_alert_toggles_on_each_tick(fix: ReminderFixture) -> None:
    fix.clock.set_time(13, 0)
    reminder = fix.create()
    fix.clock.set_time(14, 0)

    reminder.tick()  # first tick — on
    assert fix.buzzer.on is True
    assert fix.led.on is True

    reminder.tick()  # second tick — off
    assert fix.buzzer.on is False
    assert fix.led.on is False

    reminder.tick()  # third tick — on again
    assert fix.buzzer.on is True
    assert fix.led.on is True
