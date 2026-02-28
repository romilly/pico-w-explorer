from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER

display = PicoGraphics(display=DISPLAY_PICO_W_EXPLORER)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
PINK = display.create_pen(255, 192, 203)
BLUE = display.create_pen(0, 0, 255)
RED = display.create_pen(255, 0, 0)

display.set_pen(WHITE)
display.clear()

display.set_pen(BLACK)
display.line(120, 60, 120, 180)

display.set_pen(PINK)
display.circle(120, 40, 20)
display.set_pen(BLUE)
display.circle(110, 35, 4)  # Left eye
display.circle(130, 35, 4)  # Right eye
display.set_pen(RED)
display.line(110, 50, 130, 50)  # Mouth

display.set_pen(BLACK)
display.line(120, 70, 80, 110)  # Left arm
display.line(80, 110, 70, 100)  # Left fingers
display.line(80, 110, 90, 100)
display.line(120, 70, 160, 110)  # Right arm
display.line(160, 110, 150, 100)  # Right fingers
display.line(160, 110, 170, 100)

display.line(120, 180, 80, 230)  # Left leg
display.line(80, 230, 70, 230)  # Left foot
display.line(120, 180, 160, 230)  # Right leg
display.line(160, 230, 170, 230)  # Right foot

display.update()
