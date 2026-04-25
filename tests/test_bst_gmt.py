from pico_w_explorer.bst_gmt import utc_to_uk


def test_summer_utc_shifts_to_bst() -> None:
    result, zone = utc_to_uk((2026, 7, 15, 12, 0, 0, 0, 0))
    assert result[:6] == (2026, 7, 15, 13, 0, 0)
    assert zone == "BST"


def test_winter_utc_unchanged_gmt() -> None:
    result, zone = utc_to_uk((2026, 12, 15, 12, 0, 0, 0, 0))
    assert result[:6] == (2026, 12, 15, 12, 0, 0)
    assert zone == "GMT"


def test_day_before_bst_start_is_gmt() -> None:
    # In 2026, last Sunday of March is the 29th. The 28th must still be GMT.
    result, zone = utc_to_uk((2026, 3, 28, 12, 0, 0, 0, 0))
    assert result[:6] == (2026, 3, 28, 12, 0, 0)
    assert zone == "GMT"


def test_bst_start_day_before_0100_is_gmt() -> None:
    result, zone = utc_to_uk((2026, 3, 29, 0, 30, 0, 0, 0))
    assert result[:6] == (2026, 3, 29, 0, 30, 0)
    assert zone == "GMT"


def test_bst_start_day_at_0100_becomes_bst() -> None:
    result, zone = utc_to_uk((2026, 3, 29, 1, 0, 0, 0, 0))
    assert result[:6] == (2026, 3, 29, 2, 0, 0)
    assert zone == "BST"


def test_day_before_bst_end_is_bst() -> None:
    # In 2026, last Sunday of October is the 25th. The 24th must still be BST.
    result, zone = utc_to_uk((2026, 10, 24, 12, 0, 0, 0, 0))
    assert result[:6] == (2026, 10, 24, 13, 0, 0)
    assert zone == "BST"


def test_bst_end_day_before_0100_utc_still_bst() -> None:
    result, zone = utc_to_uk((2026, 10, 25, 0, 30, 0, 0, 0))
    assert result[:6] == (2026, 10, 25, 1, 30, 0)
    assert zone == "BST"


def test_bst_end_day_at_0100_utc_back_to_gmt() -> None:
    result, zone = utc_to_uk((2026, 10, 25, 1, 0, 0, 0, 0))
    assert result[:6] == (2026, 10, 25, 1, 0, 0)
    assert zone == "GMT"


def test_bst_shift_crosses_midnight() -> None:
    result, zone = utc_to_uk((2026, 7, 15, 23, 30, 0, 0, 0))
    assert result[:6] == (2026, 7, 16, 0, 30, 0)
    assert zone == "BST"


def test_weekday_uses_monday_zero_convention() -> None:
    # 2026-04-25 is a Saturday → 5 in Mon=0..Sun=6.
    result, _zone = utc_to_uk((2026, 4, 25, 10, 0, 0, 0, 0))
    assert result[6] == 5


def test_yearday_is_set_for_converted_date() -> None:
    # 2026-01-31 12:00 GMT → yearday 31.
    result, _zone = utc_to_uk((2026, 1, 31, 12, 0, 0, 0, 0))
    assert result[7] == 31
