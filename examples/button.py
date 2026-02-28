import time
from pimoroni import Button, Speaker
from machine import Pin

button_a = Button(6)

# pull GP8 high to enable speaker
amp_en = Pin(8, Pin.OUT)
amp_en.on()

# Create a speaker on pin 22
speaker = Speaker(22)

frequency = 440


while True:
    if button_a.is_pressed:
        speaker.set_tone(frequency)
        time.sleep(0.1)
        speaker.set_tone(-1)
    else:
        time.sleep(0.1)
