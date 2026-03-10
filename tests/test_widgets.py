from hamcrest import assert_that, equal_to

from pico_w_explorer.colour import BLACK, RED, WHITE
from pico_w_explorer.text_spec import TextSpec
from pico_w_explorer.widgets import Text
from tests.adapters.fake_display import FakeDisplay
from tests.matchers import rect, rect_list


def test_text_widget_clears_area_with_explicit_width() -> None:
    display = FakeDisplay()
    widget = Text(display, 10, 20, width=150)

    widget.text("hello")

    assert_that(display.rects, rect_list(
        rect(x=10, width=150, colour=BLACK)
    ))


def test_text_drawn_one_pixel_below_widget_position() -> None:
    display = FakeDisplay()
    widget = Text(display, 10, 20, width=150)

    widget.text("hello")

    assert_that(display.last_y, equal_to(21))


def test_text_widget_passes_text_spec_to_display() -> None:
    display = FakeDisplay()
    spec = TextSpec(colour=RED)
    widget = Text(display, 10, 20, width=100, text_spec=spec)

    widget.text("hello")

    assert display.last_text_spec is spec


def test_text_widget_defaults_to_white() -> None:
    display = FakeDisplay()
    widget = Text(display, 10, 20, width=100)

    widget.text("hello")

    assert display.last_colour() is WHITE
