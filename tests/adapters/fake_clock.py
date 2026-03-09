from pico_w_explorer.ports import ClockPort


class FakeClock(ClockPort):
    def __init__(self, hour: int = 0, minute: int = 0, second: int = 0, day: int = 1) -> None:
        self._hour = hour
        self._minute = minute
        self._second = second
        self._day = day

    def set_time(self, hour: int, minute: int, second: int = 0) -> None:
        self._hour = hour
        self._minute = minute
        self._second = second

    def set_day(self, day: int) -> None:
        self._day = day

    def current_time(self) -> tuple[int, int, int]:
        return (self._hour, self._minute, self._second)

    def tick(self) -> None:
        self._minute += 1
        if self._minute >= 60:
            self._minute = 0
            self._hour += 1
            if self._hour >= 24:
                self._hour = 0
                self._day += 1

    def current_date(self) -> int:
        return self._day
