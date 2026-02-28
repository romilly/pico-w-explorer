from machine import Pin  # type: ignore[import-not-found]
from pimoroni import Speaker  # type: ignore[import-not-found]

from pico_w_explorer.ports import BuzzerPort


class PicoBuzzer(BuzzerPort):
    def __init__(self, frequency: int = 440) -> None:
        self._amp_en = Pin(8, Pin.OUT)
        self._amp_en.on()
        self._speaker = Speaker(22)
        self._frequency = frequency

    def beep_on(self) -> None:
        self._speaker.set_tone(self._frequency)

    def beep_off(self) -> None:
        self._speaker.set_tone(-1)
