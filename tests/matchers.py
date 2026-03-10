"""Custom PyHamcrest matchers for the test suite."""

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description

from pico_w_explorer.colour import Colour


class IsRectMatcher(BaseMatcher[tuple[int, int, int, int, Colour]]):
    """Matcher for display rectangle tuples with optional property checks."""

    def __init__(
        self,
        x: int | None = None,
        y: int | None = None,
        width: int | None = None,
        height: int | None = None,
        colour: Colour | None = None,
    ):
        self.expected_x = x
        self.expected_y = y
        self.expected_width = width
        self.expected_height = height
        self.expected_colour = colour

    def _matches(self, item: object) -> bool:
        if not isinstance(item, tuple) or len(item) != 5:
            return False
        actual_x, actual_y, actual_width, actual_height, actual_colour = item
        if self.expected_x is not None and actual_x != self.expected_x:
            return False
        if self.expected_y is not None and actual_y != self.expected_y:
            return False
        if self.expected_width is not None and actual_width != self.expected_width:
            return False
        if self.expected_height is not None and actual_height != self.expected_height:
            return False
        if self.expected_colour is not None and actual_colour != self.expected_colour:
            return False
        return True

    def describe_to(self, description: Description) -> None:
        parts = ["a rect"]
        if self.expected_x is not None:
            parts.append(f"with x={self.expected_x}")
        if self.expected_y is not None:
            parts.append(f"with y={self.expected_y}")
        if self.expected_width is not None:
            parts.append(f"with width={self.expected_width}")
        if self.expected_height is not None:
            parts.append(f"with height={self.expected_height}")
        if self.expected_colour is not None:
            parts.append(f"with colour={self.expected_colour!r}")
        description.append_text(" ".join(parts))

    def describe_mismatch(self, item: object, mismatch_description: Description) -> None:
        if not isinstance(item, tuple) or len(item) != 5:
            mismatch_description.append_text(f"was {item!r}")
            return
        actual_x, actual_y, actual_width, actual_height, actual_colour = item
        if self.expected_x is not None and actual_x != self.expected_x:
            mismatch_description.append_text(f"had x={actual_x}")
        elif self.expected_y is not None and actual_y != self.expected_y:
            mismatch_description.append_text(f"had y={actual_y}")
        elif self.expected_width is not None and actual_width != self.expected_width:
            mismatch_description.append_text(f"had width={actual_width}")
        elif self.expected_height is not None and actual_height != self.expected_height:
            mismatch_description.append_text(f"had height={actual_height}")
        elif self.expected_colour is not None and actual_colour != self.expected_colour:
            mismatch_description.append_text(f"had colour={actual_colour!r}")


def rect(
    x: int | None = None,
    y: int | None = None,
    width: int | None = None,
    height: int | None = None,
    colour: Colour | None = None,
) -> IsRectMatcher:
    """Match a display rectangle with optional property checks."""
    return IsRectMatcher(x=x, y=y, width=width, height=height, colour=colour)


class IsRectListMatcher(BaseMatcher[list[tuple[int, int, int, int, Colour]]]):
    """Matcher for a list of rects containing specific rects in order."""

    def __init__(self, *matchers: IsRectMatcher):
        self.matchers = matchers

    def _matches(self, item: object) -> bool:
        if not isinstance(item, list):
            return False
        if len(item) != len(self.matchers):
            return False
        return all(m._matches(r) for m, r in zip(self.matchers, item))

    def describe_to(self, description: Description) -> None:
        description.append_text("a rect list containing ")
        for i, matcher in enumerate(self.matchers):
            if i > 0:
                description.append_text(", ")
            matcher.describe_to(description)

    def describe_mismatch(self, item: object, mismatch_description: Description) -> None:
        if not isinstance(item, list):
            mismatch_description.append_text(f"was {type(item).__name__}")
        elif len(item) != len(self.matchers):
            mismatch_description.append_text(
                f"had {len(item)} rects instead of {len(self.matchers)}"
            )
        else:
            for i, (matcher, actual) in enumerate(zip(self.matchers, item)):
                if not matcher._matches(actual):
                    mismatch_description.append_text(f"rect[{i}] ")
                    matcher.describe_mismatch(actual, mismatch_description)
                    return


def rect_list(*matchers: IsRectMatcher) -> IsRectListMatcher:
    """Match a list of rects containing exactly the specified rects in order."""
    return IsRectListMatcher(*matchers)
