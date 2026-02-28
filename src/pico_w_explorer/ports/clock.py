class ClockPort:
    def current_time(self) -> tuple[int, int]:
        raise NotImplementedError

    def current_date(self) -> int:
        raise NotImplementedError
