import time

from pico_w_explorer.adapters import PicoBuzzer, PicoButton, PicoClock, PicoLed
from pico_w_explorer.focus_reminder import FocusReminder

SSID = "REDACTED_SSID"
PASSWORD = "REDACTED_PASSWORD"
REMINDER_HOUR = 15
REMINDER_MINUTE = 8
TICK_INTERVAL = 0.5

clock = PicoClock(SSID, PASSWORD)
buzzer = PicoBuzzer()
led = PicoLed()
button = PicoButton()

reminder = FocusReminder(clock, buzzer, led, button, REMINDER_HOUR, REMINDER_MINUTE)

while True:
    reminder.tick()
    time.sleep(TICK_INTERVAL)
