import time
import network  # type: ignore[import-not-found]
import ntptime  # type: ignore[import-not-found]

from pico_w_explorer.bst_gmt import utc_to_uk
from pico_w_explorer.ports import ClockPort


class PicoClock(ClockPort):
    def __init__(self, ssid: str, password: str) -> None:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
        ntptime.settime()

    def _local(self) -> tuple[int, int, int, int, int, int, int, int]:
        local, _zone = utc_to_uk(time.localtime())
        return local

    def current_time(self) -> tuple[int, int, int]:
        t = self._local()
        return (t[3], t[4], t[5])

    def current_date(self) -> int:
        return self._local()[7]

    def weekday(self) -> int:
        return self._local()[6]
