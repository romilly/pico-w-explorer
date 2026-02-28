# Importing Libraries
from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER
import machine
import time
from pimoroni import Analog

# Initialize the Display
display = PicoGraphics(display=DISPLAY_PICO_W_EXPLORER)

# Define Colors
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

# Set Font
display.set_font('bitmap8')

# E12 Series (with a tolerance of ±10%)
E12_SERIES = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

colors = ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'gray', 'white']
multiplier_codes = ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet']

color_codes = {
    'black': display.create_pen(0, 0, 0),
    'brown': display.create_pen(165, 42, 42),
    'red': display.create_pen(255, 0, 0),
    'orange': display.create_pen(255, 165, 0),
    'yellow': display.create_pen(255, 255, 0),
    'green': display.create_pen(0, 128, 0),
    'blue': display.create_pen(0, 0, 255),
    'violet': display.create_pen(238, 130, 238),
    'gray': display.create_pen(128, 128, 128),
    'white': display.create_pen(255, 255, 255),
    'gold': display.create_pen(255, 215, 0)
}


# Function to Calculate Resistor Color Bands
def resistor_color_bands(resistance):
    # E12 series values
    e12_values = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
    # Color codes
    multiplier_codes = ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet']

    # Calculate the base value and multiplier
    base_value = resistance
    multiplier = 0
    while base_value >= 100:
        base_value /= 10
        multiplier += 1

    # Find the closest E12 value
    closest_value = min(e12_values, key=lambda x:abs(x-base_value))

    # Calculate the color bands
    first_band = colors[int(closest_value / 10)]
    second_band = colors[closest_value % 10]
    multiplier_band = multiplier_codes[multiplier]
    tolerance_band = 'gold'  # 5% tolerance for E12 resistors

    return [first_band, second_band, multiplier_band, tolerance_band]

# Function to Draw Resistor on Display
def draw_resistor(tolerance, *color_bands):
    # Draw the resistor body
    gray_pen = display.create_pen(192, 192, 192)  # Gray color for the resistor body
    display.set_pen(gray_pen)
    display.rectangle(80, 90, 80, 20)

    # Draw the silver wires on the left and right of the resistor
    silver_pen = display.create_pen(192, 192, 192)  # Silver color for the wires
    display.set_pen(silver_pen)
    display.rectangle(50, 99, 30, 2)  # Left wire
    display.rectangle(170, 99, 30, 2)  # Right wire

    # Draw the color bands
    for i, color in enumerate(color_bands):
        display.set_pen(color_codes[color])
        display.rectangle(90 + i*20, 90, 10, 20)
    display.set_pen(color_codes[tolerance])
    display.rectangle(160, 90, 10, 20)

    # Update the display
    display.update()


# Function to Find Closest E12 Resistor Value
def find_closest_e12(resistance):
    # Create a list of all E12 resistances within a reasonable range
    e12_values = []
    for power in range(1, 7):
        e12_values.extend([val * 10 ** power for val in E12_SERIES])

    # Find the closest E12 resistance to the given resistance
    closest_e12 = min(e12_values, key=lambda x: abs(x - resistance))

    return closest_e12

# Configure Analog Input
adc = Analog(27) # ADC1
R1 = 10000  # known resistance
VIN = 3.3  # input voltage

# Main Loop
while True:
    # Read voltage
    vout = adc.read_voltage()

    # Calculate unknown resistance
    R2 = float('%.2g' % (R1 * ((VIN / vout) - 1)))

    # Clear the display
    display.set_pen(WHITE)
    display.clear()

    # Write the resistance to the display
    display.set_pen(BLACK)
    display.text("R2: " + str(R2) + " Ohm", 10, 10, 240, 2)

    R_CLOSEST = find_closest_e12(R2)
    display.text("CLOSEST E12: " + str(R_CLOSEST) + " Ohm", 10, 30, 240, 2)

    c1, c2, c3, tolerance = resistor_color_bands(R_CLOSEST)
    draw_resistor(tolerance, c1, c2, c3)

    # Update the display
    display.update()