from hamcrest import assert_that, equal_to, has_length

from pico_w_explorer.colour import BLACK
from pico_w_explorer.widgets import Text
from tests.adapters.fake_display import FakeDisplay


def test_text_widget_clears_area_with_explicit_width() -> None:
    display = FakeDisplay()
    widget = Text(display, 10, 20, width=150)

    widget.text("hello")

    assert_that(display.rects, has_length(1))
    x, y, width, height, colour = display.rects[0]
    assert_that(x, equal_to(10))
    assert_that(width, equal_to(150))
    assert_that(colour, equal_to(BLACK))


def test_text_drawn_one_pixel_below_widget_position() -> None:
    display = FakeDisplay()
    widget = Text(display, 10, 20, width=150)

    widget.text("hello")

    assert_that(display.last_y, equal_to(21))
