
import calendar

WEEKDAY_LABELS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def month_grid(year, month):
    cal = calendar.Calendar(firstweekday=6)  # 6 => weeks start on Sunday
    weeks = []
    week = []
    for d in cal.itermonthdates(year, month):
        week.append(d)
        if len(week) == 7:
            weeks.append(week)
            week = []
    return weeks


def add_months(year, month, delta):
    """Step the given (year, month) forward/backward by `delta` months."""
    index = month - 1 + delta
    new_year = year + index // 12
    new_month = index % 12 + 1
    return new_year, new_month
