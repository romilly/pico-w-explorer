from pico_w_explorer.focus_reminder import FocusReminder
from tests.adapters.fake_buzzer import FakeBuzzer
from tests.adapters.fake_button import FakeButton
from tests.adapters.fake_clock import FakeClock
from tests.adapters.fake_led import FakeLed


def test_full_reminder_lifecycle() -> None:
    clock = FakeClock()
    buzzer = FakeBuzzer()
    led = FakeLed()
    button = FakeButton()
    reminder = FocusReminder(clock, buzzer, led, button, reminder_hour=14, reminder_minute=0)

    # Before reminder time — no alert
    clock.set_time(13, 0)
    reminder.tick()
    assert buzzer.on is False
    assert led.on is False

    # At reminder time — alert activates
    clock.set_time(14, 0)
    reminder.tick()
    assert buzzer.on is True
    assert led.on is True

    # Button press — alert dismissed
    button.press()
    reminder.tick()
    assert buzzer.on is False
    assert led.on is False

    # Stays dismissed after button release
    button.release()
    reminder.tick()
    assert buzzer.on is False
    assert led.on is False
