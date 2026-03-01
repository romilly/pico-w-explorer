from hamcrest import assert_that, equal_to

from tests.builders import ApplicationBuilder


def test_start_displays_connecting_message() -> None:
    builder = ApplicationBuilder()
    app = builder.build()

    app.start()

    assert_that(builder.display.texts[0], equal_to("Connecting to WiFi..."))


def test_start_displays_clock_sync_info() -> None:
    builder = ApplicationBuilder()
    builder.clock.set_time(10, 30)
    app = builder.build()

    app.start()

    assert_that(builder.display.texts[1],
                equal_to("Clock synced\n10:30\nReminder at 14:00"))


def test_start_displays_running_message() -> None:
    builder = ApplicationBuilder()
    app = builder.build()

    app.start()

    assert_that(builder.display.texts[2],
                equal_to("Running...\nReminder at 14:00"))


def test_tick_activates_alert_at_reminder_time() -> None:
    builder = ApplicationBuilder()
    builder.clock.set_time(14, 0)
    app = builder.build()
    app.start()

    app.tick()

    assert builder.buzzer.on is True
    assert builder.led.on is True


def test_tick_no_alert_before_reminder_time() -> None:
    builder = ApplicationBuilder()
    builder.clock.set_time(13, 0)
    app = builder.build()
    app.start()

    app.tick()

    assert builder.buzzer.on is False
    assert builder.led.on is False


def test_builder_custom_reminder_time() -> None:
    builder = ApplicationBuilder().with_reminder_time(9, 30)
    builder.clock.set_time(9, 30)
    app = builder.build()
    app.start()

    app.tick()

    assert builder.buzzer.on is True


def test_start_displays_custom_reminder_time() -> None:
    builder = ApplicationBuilder().with_reminder_time(9, 30)
    builder.clock.set_time(8, 15)
    app = builder.build()

    app.start()

    assert_that(builder.display.texts[1],
                equal_to("Clock synced\n08:15\nReminder at 09:30"))
    assert_that(builder.display.texts[2],
                equal_to("Running...\nReminder at 09:30"))
