from pico_w_explorer.ports import ClockPort


class FakeClock(ClockPort):
    def __init__(self, hour: int = 0, minute: int = 0, day: int = 1) -> None:
        self._hour = hour
        self._minute = minute
        self._day = day

    def set_time(self, hour: int, minute: int) -> None:
        self._hour = hour
        self._minute = minute

    def set_day(self, day: int) -> None:
        self._day = day

    def current_time(self) -> tuple[int, int]:
        return (self._hour, self._minute)

    def current_date(self) -> int:
        return self._day
