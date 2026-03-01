from tests.builders import ApplicationBuilder


def test_full_application_lifecycle() -> None:
    builder = ApplicationBuilder().with_time(13, 0)
    app = builder.build()
    app.start()

    # Before reminder time — no alert
    app.tick()
    assert builder.buzzer.on is False
    assert builder.led.on is False

    # At reminder time — alert activates
    builder.clock.set_time(14, 0)
    app.tick()
    assert builder.buzzer.on is True
    assert builder.led.on is True

    # Button press — alert dismissed
    builder.button.press()
    app.tick()
    assert builder.buzzer.on is False
    assert builder.led.on is False

    # Stays dismissed after button release
    builder.button.release()
    app.tick()
    assert builder.buzzer.on is False
    assert builder.led.on is False
