from tests.adapters.fake_clock import FakeClock


def test_tick_advances_minute() -> None:
    clock = FakeClock(hour=10, minute=30)
    clock.tick()
    assert clock.current_time() == (10, 31)


def test_tick_rolls_over_hour() -> None:
    clock = FakeClock(hour=10, minute=59)
    clock.tick()
    assert clock.current_time() == (11, 0)


def test_tick_rolls_over_day() -> None:
    clock = FakeClock(hour=23, minute=59, day=5)
    clock.tick()
    assert clock.current_time() == (0, 0)
    assert clock.current_date() == 6
