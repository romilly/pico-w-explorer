def utc_to_uk(dt):
    """Convert UTC time tuple to UK local time.
    Takes any time tuple (at least 6 elements).
    Returns ((year, month, day, hour, minute, second, weekday, yearday), zone)
    """
    year, month, day, hour, minute, second = dt[:6]
    
    def day_of_week(y, m, d):
        if m < 3:
            m += 12
            y -= 1
        return (d + 13*(m+1)//5 + y + y//4 - y//100 + y//400) % 7

    def last_sunday(y, m):
        for d in range(31, 24, -1):
            if day_of_week(y, m, d) == 6:
                return d

    bst_start = last_sunday(year, 3)
    bst_end = last_sunday(year, 10)

    bst = False
    if month > 3 and month < 10:
        bst = True
    elif month == 3:
        bst = (day > bst_start) or (day == bst_start and hour >= 1)
    elif month == 10:
        bst = (day < bst_end) or (day == bst_end and hour < 1)

    if bst:
        hour += 1
        if hour >= 24:
            hour -= 24
            day += 1
            days_in_month = [0,31,0,31,30,31,30,31,31,30,31,30,31]
            if day > days_in_month[month]:
                day = 1
                month += 1

    weekday = day_of_week(year, month, day)
    zone = 'BST' if bst else 'GMT'
    return (year, month, day, hour, minute, second, weekday, 0), zone