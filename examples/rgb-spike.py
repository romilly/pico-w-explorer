from machine import Pin
from time import sleep

red = Pin(0, Pin.OUT)
blue = Pin(1, Pin.OUT)
green = Pin(2, Pin.OUT)
leds = [red, blue, green]

for led in leds:
    led.on()
    sleep(1)
    led.off()

