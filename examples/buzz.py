from machine import Pin
from pimoroni import Speaker
import time

# pull GP8 high to enable speaker
amp_en = Pin(8, Pin.OUT)
amp_en.on()

# Create a speaker on pin 22
speaker = Speaker(22)

frequency = 440
speaker.set_tone(frequency)
time.sleep(1)
speaker.set_tone(-1)
