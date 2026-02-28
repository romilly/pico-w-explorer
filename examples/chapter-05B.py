import time

from pimoroni import Analog
from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER

pot = Analog(26)  # assuming the potentiometer is connected to pin 26 (A0)

display = PicoGraphics(display=DISPLAY_PICO_W_EXPLORER)

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

display.set_font("bitmap8")
display.set_pen(BLACK)

while True:
    voltage = pot.read_voltage()

    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)

    display.text("{:.2f} Volts".format(voltage), 20, 50, scale=3)

    display.update()

    time.sleep(0.1)