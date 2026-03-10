import pytest

from pico_w_explorer.colour import WHITE, RED
from pico_w_explorer.text_spec import TextSpec


def test_defaults() -> None:
    spec = TextSpec()
    assert spec.font == "sans"
    assert spec.colour is WHITE
    assert spec.thickness == 2
    assert spec.scale == 1


def test_custom_values() -> None:
    spec = TextSpec(font="gothic", colour=RED, thickness=3, scale=1.5)
    assert spec.font == "gothic"
    assert spec.colour is RED
    assert spec.thickness == 3
    assert spec.scale == 1.5


def test_rejects_invalid_font() -> None:
    with pytest.raises(ValueError):
        TextSpec(font="comic")
