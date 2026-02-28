import time

import WIFI_CONFIG  # type: ignore[import-not-found]

from pico_w_explorer.adapters import PicoBuzzer, PicoButton, PicoClock, PicoDisplay, PicoLed
from pico_w_explorer.focus_reminder import FocusReminder

REMINDER_HOUR = 16
REMINDER_MINUTE = 0
TICK_INTERVAL = 0.5

display = PicoDisplay()

display.show_text("Connecting to WiFi...")
clock = PicoClock(WIFI_CONFIG.SSID, WIFI_CONFIG.PASSWORD)
hour, minute = clock.current_time()
display.show_text("Clock synced\n%02d:%02d\nReminder at %02d:%02d" % (hour, minute, REMINDER_HOUR, REMINDER_MINUTE))

buzzer = PicoBuzzer()
led = PicoLed()
button = PicoButton()

reminder = FocusReminder(clock, buzzer, led, button, REMINDER_HOUR, REMINDER_MINUTE)

display.show_text("Running...\nReminder at %02d:%02d" % (REMINDER_HOUR, REMINDER_MINUTE))
while True:
    reminder.tick()
    time.sleep(TICK_INTERVAL)
