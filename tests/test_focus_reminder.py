import pytest

from pico_w_explorer.focus_reminder import FocusReminder
from tests.adapters.fake_buzzer import FakeBuzzer
from tests.adapters.fake_button import FakeButton
from tests.adapters.fake_clock import FakeClock
from tests.adapters.fake_led import FakeLed

TWO_PM: tuple[int, int] = (14, 0)
SINGLE_REMINDER: list[tuple[int, int]] = [TWO_PM]


class ReminderFixture:
    def __init__(self) -> None:
        self.clock = FakeClock()
        self.buzzer = FakeBuzzer()
        self.led = FakeLed()
        self.button = FakeButton()
        self.reminder = FocusReminder(
            self.clock, self.buzzer, self.led, self.button,
            reminder_times=[],
        )

    def create(
        self,
        reminder_times: list[tuple[int, int]],
        alert_duration: int = 20,
    ) -> FocusReminder:
        self.reminder = FocusReminder(
            self.clock, self.buzzer, self.led, self.button,
            reminder_times=reminder_times,
            alert_duration=alert_duration,
        )
        return self.reminder


@pytest.fixture
def fix() -> ReminderFixture:
    return ReminderFixture()


@pytest.fixture
def single(fix: ReminderFixture) -> ReminderFixture:
    fix.create(SINGLE_REMINDER)
    return fix


@pytest.fixture
def short(fix: ReminderFixture) -> ReminderFixture:
    fix.create(SINGLE_REMINDER, alert_duration=4)
    return fix


def test_no_alert_before_reminder_time(single: ReminderFixture) -> None:
    single.clock.set_time(13, 0)

    single.reminder.tick()

    assert single.buzzer.on is False
    assert single.led.on is False


def test_alert_starts_at_reminder_time(single: ReminderFixture) -> None:
    single.clock.set_time(14, 0)

    single.reminder.tick()

    assert single.buzzer.on is True
    assert single.led.on is True


def test_alert_continues_past_reminder_time(single: ReminderFixture) -> None:
    single.clock.set_time(14, 5)

    single.reminder.tick()

    assert single.buzzer.on is True
    assert single.led.on is True


def test_button_press_dismisses_alert(single: ReminderFixture) -> None:
    single.clock.set_time(14, 0)

    single.reminder.tick()  # starts alerting
    single.button.press()
    single.reminder.tick()  # should dismiss

    assert single.buzzer.on is False
    assert single.led.on is False


def test_alert_stays_dismissed_after_button_release(single: ReminderFixture) -> None:
    single.clock.set_time(14, 0)

    single.reminder.tick()  # starts alerting
    single.button.press()
    single.reminder.tick()  # dismisses
    single.button.release()
    single.reminder.tick()  # should stay silent

    assert single.buzzer.on is False
    assert single.led.on is False


def test_dismissed_resets_next_day(single: ReminderFixture) -> None:
    single.clock.set_time(14, 0)

    single.reminder.tick()  # starts alerting
    single.button.press()
    single.reminder.tick()  # dismisses
    single.button.release()

    # Next day, before reminder time — still silent
    single.clock.set_day(2)
    single.clock.set_time(13, 0)
    single.reminder.tick()
    assert single.buzzer.on is False
    assert single.led.on is False

    # Next day, at reminder time — alert fires again
    single.clock.set_time(14, 0)
    single.reminder.tick()
    assert single.buzzer.on is True
    assert single.led.on is True


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
    reminder = fix.create(SINGLE_REMINDER)

    reminder.tick()

    assert fix.buzzer.on is False
    assert fix.led.on is False


def test_alert_auto_dismisses_after_duration(short: ReminderFixture) -> None:
    short.clock.set_time(14, 0)

    for _ in range(4):
        short.reminder.tick()

    # After 4 ticks, alert should be auto-dismissed
    short.reminder.tick()
    assert short.buzzer.on is False
    assert short.led.on is False

    # Should stay dismissed
    short.reminder.tick()
    assert short.buzzer.on is False
    assert short.led.on is False


def test_auto_dismiss_lets_next_alert_fire(fix: ReminderFixture) -> None:
    fix.clock.set_time(13, 0)
    reminder = fix.create(reminder_times=[(14, 0), (16, 0)], alert_duration=4)
    fix.clock.set_time(14, 0)

    # Let first alert auto-dismiss
    for _ in range(5):
        reminder.tick()

    # Advance to 16:00 — second alert should fire
    fix.clock.set_time(16, 0)
    reminder.tick()
    assert fix.buzzer.on is True
    assert fix.led.on is True


def test_alert_toggles_on_each_tick(single: ReminderFixture) -> None:
    single.clock.set_time(14, 0)

    single.reminder.tick()  # first tick — on
    assert single.buzzer.on is True
    assert single.led.on is True

    single.reminder.tick()  # second tick — off
    assert single.buzzer.on is False
    assert single.led.on is False

    single.reminder.tick()  # third tick — on again
    assert single.buzzer.on is True
    assert single.led.on is True
