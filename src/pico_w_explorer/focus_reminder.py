from pico_w_explorer.ports import BuzzerPort, ButtonPort, ClockPort, LedPort


class AlertState:
    def __init__(self, hour: int, minute: int) -> None:
        self.hour = hour
        self.minute = minute
        self.dismissed = False
        self.dismissed_on_day: int | None = None

    def reset_if_new_day(self, today: int) -> None:
        if self.dismissed and today != self.dismissed_on_day:
            self.dismissed = False
            self.dismissed_on_day = None

    def is_due(self, hour: int, minute: int) -> bool:
        return (hour, minute) >= (self.hour, self.minute)


class FocusReminder:
    def __init__(
        self,
        clock: ClockPort,
        buzzer: BuzzerPort,
        led: LedPort,
        button: ButtonPort,
        reminder_times: list[tuple[int, int]],
    ) -> None:
        self._clock = clock
        self._buzzer = buzzer
        self._led = led
        self._button = button
        self._states = [AlertState(h, m) for h, m in reminder_times]
        self._alert_on = False

    def tick(self) -> None:
        hour, minute, _second = self._clock.current_time()
        today = self._clock.current_date()

        for state in self._states:
            state.reset_if_new_day(today)

        active = self._active_alert(hour, minute)

        if self._button.is_pressed() and active is not None:
            active.dismissed = True
            active.dismissed_on_day = today
            self._alert_on = False
            self._buzzer.beep_off()
            self._led.flash_off()
        elif active is not None:
            self._alert_on = not self._alert_on
            if self._alert_on:
                self._buzzer.beep_on()
                self._led.flash_on()
            else:
                self._buzzer.beep_off()
                self._led.flash_off()
        else:
            self._alert_on = False
            self._buzzer.beep_off()
            self._led.flash_off()

    def _active_alert(self, hour: int, minute: int) -> 'AlertState | None':
        due = [s for s in self._states if not s.dismissed and s.is_due(hour, minute)]
        if not due:
            return None
        return min(due, key=lambda s: (s.hour, s.minute))
