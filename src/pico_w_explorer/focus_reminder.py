from pico_w_explorer.ports import BuzzerPort, ButtonPort, ClockPort, LedPort


class FocusReminder:
    def __init__(
        self,
        clock: ClockPort,
        buzzer: BuzzerPort,
        led: LedPort,
        button: ButtonPort,
        reminder_hour: int,
        reminder_minute: int,
    ) -> None:
        self._clock = clock
        self._buzzer = buzzer
        self._led = led
        self._button = button
        self._reminder_hour = reminder_hour
        self._reminder_minute = reminder_minute
        self._dismissed = False
        self._dismissed_on_day: int | None = None
        self._alert_on = False

    def tick(self) -> None:
        hour, minute = self._clock.current_time()
        today = self._clock.current_date()
        if self._dismissed and today != self._dismissed_on_day:
            self._dismissed = False
            self._dismissed_on_day = None
        if self._button.is_pressed():
            self._dismissed = True
            self._dismissed_on_day = today
            self._alert_on = False
            self._buzzer.beep_off()
            self._led.flash_off()
        elif not self._dismissed and (hour, minute) >= (self._reminder_hour, self._reminder_minute):
            self._alert_on = not self._alert_on
            if self._alert_on:
                self._buzzer.beep_on()
                self._led.flash_on()
            else:
                self._buzzer.beep_off()
                self._led.flash_off()
