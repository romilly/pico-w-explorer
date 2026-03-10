from pico_w_explorer.colour import Colour


def test_rgb_returns_tuple() -> None:
    colour = Colour(255, 128, 0)
    assert colour.rgb() == (255, 128, 0)
