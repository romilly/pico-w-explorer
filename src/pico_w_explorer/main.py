import WIFI_CONFIG  # type: ignore[import-not-found]

from pico_w_explorer.adapters import PicoBuzzer, PicoButton, PicoClock, PicoDisplay, PicoLed
from pico_w_explorer.application import Application, ApplicationConfig

config = ApplicationConfig(
    clock=PicoClock(WIFI_CONFIG.SSID, WIFI_CONFIG.PASSWORD),
    buzzer=PicoBuzzer(),
    led=PicoLed(),
    button=PicoButton(),
    display=PicoDisplay(),
    reminder_times=[(12, 45), (14, 0), (16, 0)],
)
app = Application(config)
app.run()
