import time
import network  # type: ignore[import-not-found]
import ntptime  # type: ignore[import-not-found]

from pico_w_explorer.ports import ClockPort


class PicoClock(ClockPort):
    def __init__(self, ssid: str, password: str) -> None:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
        ntptime.settime()

    def current_time(self) -> tuple[int, int, int]:
        t = time.localtime()
        return (t[3], t[4], t[5])

    def current_date(self) -> int:
        return time.localtime()[7]

    def weekday(self) -> int:
        return time.localtime()[6]
