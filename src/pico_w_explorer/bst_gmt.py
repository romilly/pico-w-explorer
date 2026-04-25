_DAYS_BEFORE_MONTH = (0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
_DAYS_IN_MONTH = (0, 31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def _is_leap(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def _yearday(year: int, month: int, day: int) -> int:
    yd = _DAYS_BEFORE_MONTH[month] + day
    if month > 2 and _is_leap(year):
        yd += 1
    return yd


def _sakamoto(year: int, month: int, day: int) -> int:
    """Return weekday with Sat=0, Sun=1, ..., Fri=6."""
    y, m = year, month
    if m < 3:
        m += 12
        y -= 1
    return (day + 13 * (m + 1) // 5 + y + y // 4 - y // 100 + y // 400) % 7


def _weekday_mon0(year: int, month: int, day: int) -> int:
    """Return weekday with Mon=0..Sun=6 (matching time.struct_time)."""
    return (_sakamoto(year, month, day) + 5) % 7


def _last_sunday(year: int, month: int) -> int:
    for d in range(31, 24, -1):
        if _sakamoto(year, month, d) == 1:
            return d
    raise AssertionError("unreachable: every month has a Sunday in its last 7 days")


def utc_to_uk(dt: tuple[int, ...]) -> tuple[tuple[int, int, int, int, int, int, int, int], str]:
    """Convert a UTC time tuple to UK local time.

    Takes any time tuple (at least 6 elements: year, month, day, hour, minute, second).
    Returns ((year, month, day, hour, minute, second, weekday, yearday), zone)
    where weekday uses Mon=0..Sun=6 and zone is 'BST' or 'GMT'.
    """
    year, month, day, hour, minute, second = dt[:6]

    bst_start = _last_sunday(year, 3)
    bst_end = _last_sunday(year, 10)

    if 3 < month < 10:
        bst = True
    elif month == 3:
        bst = (day > bst_start) or (day == bst_start and hour >= 1)
    elif month == 10:
        bst = (day < bst_end) or (day == bst_end and hour < 1)
    else:
        bst = False

    if bst:
        hour += 1
        if hour >= 24:
            hour -= 24
            day += 1
            last_day = 29 if month == 2 and _is_leap(year) else _DAYS_IN_MONTH[month]
            if day > last_day:
                day = 1
                month += 1
                if month > 12:
                    month = 1
                    year += 1

    weekday = _weekday_mon0(year, month, day)
    yearday = _yearday(year, month, day)
    zone = "BST" if bst else "GMT"
    return (year, month, day, hour, minute, second, weekday, yearday), zone
