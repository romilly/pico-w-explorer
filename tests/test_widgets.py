from hamcrest import assert_that, equal_to, has_length

from pico_w_explorer.colour import BLACK
from pico_w_explorer.widgets import Text
from tests.adapters.fake_display import FakeDisplay


def test_text_widget_clears_area_before_drawing() -> None:
    display = FakeDisplay()
    widget = Text(display, 10, 20)

    widget.text("hello")

    assert_that(display.rects, has_length(1))
    x, y, width, height, colour = display.rects[0]
    assert_that(x, equal_to(10))
    assert_that(colour, equal_to(BLACK))


def test_clear_width_uses_max_of_old_and_new() -> None:
    display = FakeDisplay()
    widget = Text(display, 10, 20)

    widget.text("long text here")  # 14 chars = 140px
    widget.text("short")           # 5 chars = 50px

    # Second clear should use old width (140) not new width (50)
    _, _, second_clear_width, _, _ = display.rects[1]
    assert_that(second_clear_width, equal_to(140 + 2))


def test_text_drawn_one_pixel_below_widget_position() -> None:
    display = FakeDisplay()
    widget = Text(display, 10, 20)

    widget.text("hello")

    assert_that(display.last_y, equal_to(21))
