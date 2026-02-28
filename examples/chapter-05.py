import machine
import time
from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER

display = PicoGraphics(display=DISPLAY_PICO_W_EXPLORER)
sensor_temp = machine.ADC(4)

WIDTH, HEIGHT = display.get_bounds()

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

conversion_factor = 3.3 / (65535)

temp_min = 10
temp_max = 30
bar_width = 5

temperatures = []

colors = [(0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 0)]

def temperature_to_color(temp):
    temp = min(temp, temp_max)
    temp = max(temp, temp_min)

    f_index = float(temp - temp_min) / float(temp_max - temp_min)
    f_index *= len(colors) - 1
    index = int(f_index)

    if index == len(colors) - 1:
        return colors[index]

    blend_b = f_index - index
    blend_a = 1.0 - blend_b

    a = colors[index]
    b = colors[index + 1]

    return [int((a[i] * blend_a) + (b[i] * blend_b)) for i in range(3)]


while True:
    display.set_pen(BLACK)
    display.clear()
    
    # the following two lines do some maths to convert the number from the temp sensor into celsius
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    temperatures.append(temperature)

    if len(temperatures) > WIDTH // bar_width:
        temperatures.pop(0)
    
    i = 0
    
    for t in temperatures:
        TEMPERATURE_COLOUR = display.create_pen(*temperature_to_color(t))
        display.set_pen(TEMPERATURE_COLOUR)
        display.rectangle(i, HEIGHT - (round(t) * 4), bar_width, HEIGHT)
        i += bar_width

    display.set_pen(WHITE)
    display.rectangle(1, 1, 100, 25)
    display.set_pen(BLACK)
    display.text("{:.2f}".format(temperature) + "c", 3, 3, 0, 3)

    display.update()
    time.sleep(5)

import time

from pimoroni import Analog
from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER

pot = Analog(26)  # assuming the potentiometer is connected to pin 26 (A0)

display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)

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