import WIFI_CONFIG  # type: ignore[import-not-found]

from pico_w_explorer.adapters import PicoBuzzer, PicoButton, PicoClock, PicoDisplay, PicoLed
from pico_w_explorer.application import Application

app = Application(
    clock=PicoClock(WIFI_CONFIG.SSID, WIFI_CONFIG.PASSWORD),
    buzzer=PicoBuzzer(),
    led=PicoLed(),
    button=PicoButton(),
    display=PicoDisplay(),
    reminder_hour=16,
    reminder_minute=0,
)
app.run()
