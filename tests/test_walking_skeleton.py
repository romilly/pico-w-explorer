from tests.builders import ApplicationBuilder


class TestFullApplicationLifecycle:
    def setup_method(self) -> None:
        builder = ApplicationBuilder().with_time(13, 0)
        self.clock = builder.clock
        self.buzzer = builder.buzzer
        self.led = builder.led
        self.button = builder.button
        self.app = builder.build()
        self.app.start()

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

    def test_full_lifecycle(self) -> None:
        # Before reminder — silent
        self.wait(minutes=30)
        self.assert_silent()

        # At reminder time (14:00) — alerting
        self.wait(minutes=30)
        self.assert_alerting()

        # Button press — dismissed
        self.press_button()
        self.wait()
        self.assert_silent()

        # Stays dismissed after release
        self.release_button()
        self.wait()
        self.assert_silent()
