from pico_w_explorer.ports import BuzzerPort, ButtonPort, ClockPort, LedPort


class AlertState:
    def __init__(self, hour: int, minute: int) -> None:
        self.hour = hour
        self.minute = minute
        self.dismissed = False
        self.dismissed_on_day: int = 0

    def reset_if_new_day(self, today: int) -> None:
        if self.dismissed and today != self.dismissed_on_day:
            self.dismissed = False
            self.dismissed_on_day = 0

    def dismiss(self, today: int) -> None:
        self.dismissed = True
        self.dismissed_on_day = today

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
        alert_duration: int = 20,
    ) -> None:
        self._clock = clock
        self._buzzer = buzzer
        self._led = led
        self._button = button
        self._states = [AlertState(h, m) for h, m in reminder_times]
        self._alert_on = False
        self._alert_duration = alert_duration
        self._alert_ticks = 0
        hour, minute, _ = clock.current_time()
        today = clock.current_date()
        for state in self._states:
            if state.is_due(hour, minute):
                state.dismiss(today)

    def tick(self) -> None:
        hour, minute, _ = self._clock.current_time()
        today = self._clock.current_date()

        for state in self._states:
            state.reset_if_new_day(today)

        active = self._active_alert(hour, minute)

        if active is None:
            self._alert_off()
            self._alert_ticks = 0
            return

        if self._button.is_pressed():
            active.dismiss(today)
            self._alert_off()
            self._alert_ticks = 0
            return

        self._alert_ticks += 1
        if self._alert_ticks > self._alert_duration:
            active.dismiss(today)
            self._alert_off()
            self._alert_ticks = 0
            return

        if self._alert_on:
            self._alert_off()
            return

        self._alert_on = True
        self._buzzer.beep_on()
        self._led.flash_on()

    def _alert_off(self) -> None:
        self._alert_on = False
        self._buzzer.beep_off()
        self._led.flash_off()

    def _active_alert(self, hour: int, minute: int) -> 'AlertState | None':
        for state in self._states:
            if not state.dismissed and state.is_due(hour, minute):
                return state
        return None
