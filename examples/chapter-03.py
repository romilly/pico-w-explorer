from pimoroni import Pin, Speaker
import time

# pull GP8 high to enable speaker
amp_en = Pin(8, Pin.OUT)
amp_en.on()

frequency = 440

speaker = Speaker(22)

speaker.set_tone(frequency)

time.sleep(1)

speaker.set_tone(-1)

import time
from pimoroni import Button, Speaker

# pull GP8 high to enable speaker
amp_en = Pin(8, Pin.OUT)
amp_en.on()

speaker = Speaker(22)
button_a = Button(6)

while True:
   if button_a.is_pressed:
        speaker.set_tone(440)
        time.sleep(0.1)
        speaker.set_tone(-1)

else:
    time.sleep(0.1)