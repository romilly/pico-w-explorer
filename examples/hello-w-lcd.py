from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER, PEN_P8

display = PicoGraphics(display=DISPLAY_PICO_W_EXPLORER)

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

display.set_pen(BLACK)
display.clear()
display.set_pen(WHITE)
display.text("Hello Pico W World", 20, 20, 200)
display.update()