import time

import WIFI_CONFIG  # type: ignore[import-not-found]

from pico_w_explorer.adapters import PicoBuzzer, PicoButton, PicoClock, PicoLed
from pico_w_explorer.focus_reminder import FocusReminder
REMINDER_HOUR = 16
REMINDER_MINUTE = 0
TICK_INTERVAL = 0.5

print("Connecting to WiFi and syncing clock...")
clock = PicoClock(WIFI_CONFIG.SSID, WIFI_CONFIG.PASSWORD)
print("Clock synced. Time:", clock.current_time(), "Day:", clock.current_date())
print(f"Reminder set for {REMINDER_HOUR:02d}:{REMINDER_MINUTE:02d}")

buzzer = PicoBuzzer()
led = PicoLed()
button = PicoButton()

reminder = FocusReminder(clock, buzzer, led, button, REMINDER_HOUR, REMINDER_MINUTE)

print("Running...")
while True:
    reminder.tick()
    time.sleep(TICK_INTERVAL)
