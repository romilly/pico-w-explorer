class ClockPort:
    def current_time(self) -> tuple[int, int, int]:
        raise NotImplementedError

    def current_date(self) -> int:
        raise NotImplementedError

    def weekday(self) -> int:
        raise NotImplementedError
