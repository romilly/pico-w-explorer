from hamcrest import assert_that, equal_to

from tests.builders import ApplicationBuilder


def test_start_displays_running_message() -> None:
    builder = ApplicationBuilder()
    app = builder.build()

    app.start()

    assert_that(builder.display.texts[0], equal_to("Running..."))


def test_start_displays_reminders_label() -> None:
    builder = ApplicationBuilder()
    app = builder.build()

    app.start()

    assert_that(builder.display.texts[1], equal_to("Reminders:"))


def test_start_displays_single_reminder_time() -> None:
    builder = ApplicationBuilder().with_reminder_time(14, 0)
    app = builder.build()

    app.start()

    assert_that(builder.display.texts[2], equal_to("14:00"))


def test_start_displays_multiple_reminder_times() -> None:
    builder = ApplicationBuilder().with_reminder_times([(9, 0), (14, 0)])
    app = builder.build()

    app.start()

    assert_that(builder.display.texts[2], equal_to("09:00, 14:00"))


def test_start_displays_custom_reminder_time() -> None:
    builder = ApplicationBuilder().with_reminder_time(9, 30)
    app = builder.build()

    app.start()

    assert_that(builder.display.texts[2], equal_to("09:30"))


def test_start_displays_current_time() -> None:
    builder = ApplicationBuilder().with_time(10, 30)
    app = builder.build()

    app.start()

    assert_that(builder.display.texts[3], equal_to("10:30"))


def test_tick_updates_time_at_new_minute() -> None:
    builder = ApplicationBuilder().with_time(10, 30)
    app = builder.build()
    app.start()
    builder.clock.set_time(10, 31, 0)

    app.tick()

    assert_that(builder.display.texts[-1], equal_to("10:31"))


def test_tick_does_not_update_time_mid_minute() -> None:
    builder = ApplicationBuilder().with_time(10, 30)
    app = builder.build()
    app.start()
    text_count_after_start = len(builder.display.texts)
    builder.clock.set_time(10, 30, 30)

    app.tick()

    assert len(builder.display.texts) == text_count_after_start


def test_tick_activates_alert_at_reminder_time() -> None:
    builder = ApplicationBuilder().with_time(14, 0)
    app = builder.build()
    app.start()

    app.tick()

    assert builder.buzzer.on is True
    assert builder.led.on is True


def test_tick_no_alert_before_reminder_time() -> None:
    builder = ApplicationBuilder().with_time(13, 0)
    app = builder.build()
    app.start()

    app.tick()

    assert builder.buzzer.on is False
    assert builder.led.on is False


def test_builder_custom_reminder_time() -> None:
    builder = ApplicationBuilder().with_reminder_time(9, 30).with_time(9, 30)
    app = builder.build()
    app.start()

    app.tick()

    assert builder.buzzer.on is True
