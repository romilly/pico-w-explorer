from pico_w_explorer.colour import Colour, WHITE, BLACK, RED, GREEN, BLUE, YELLOW
from pico_w_explorer.widgets import Text
from tests.adapters.fake_display import FakeDisplay


def test_colour_has_rgb_fields() -> None:
    colour = Colour(255, 128, 0)
    assert colour.red == 255
    assert colour.green == 128
    assert colour.blue == 0


def test_white_is_all_255() -> None:
    assert WHITE.red == 255
    assert WHITE.green == 255
    assert WHITE.blue == 255


def test_black_is_all_zero() -> None:
    assert BLACK.red == 0
    assert BLACK.green == 0
    assert BLACK.blue == 0


def test_text_widget_passes_colour_to_display() -> None:
    display = FakeDisplay()
    widget = Text(display, 10, 20, width=100, colour=RED)

    widget.text("hello")

    assert display.last_colour is RED


def test_text_widget_defaults_to_white() -> None:
    display = FakeDisplay()
    widget = Text(display, 10, 20, width=100)

    widget.text("hello")

    assert display.last_colour is WHITE
