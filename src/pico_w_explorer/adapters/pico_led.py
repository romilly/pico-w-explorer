from machine import Pin  # type: ignore[import-not-found]

from pico_w_explorer.ports import LedPort


class PicoLed(LedPort):
    def __init__(self) -> None:
        self._pin = Pin('LED', Pin.OUT)

    def flash_on(self) -> None:
        self._pin.on()

    def flash_off(self) -> None:
        self._pin.off()
