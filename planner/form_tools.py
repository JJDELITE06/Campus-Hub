# planner/form_tools.py -- small helper functions for reading web forms.
#
# Everything a browser sends us arrives as TEXT (a "string"), even dates:
#     "2026-11-20"   and   "14:30"
# These helpers turn that text into real Python date/time objects, and back.
# If the text is empty or nonsense they return None ("nothing") instead of
# crashing, and our validate() methods then report a friendly error.

from datetime import datetime


def parse_date(text):
    """Turns "2026-11-20" into a date object. Returns None if it can't."""
    try:
        # strptime = "string parse time". %Y-%m-%d describes the layout:
        # 4-digit year, month, day.
        return datetime.strptime(str(text).strip(), "%Y-%m-%d").date()
    except ValueError:
        # ValueError is what Python raises when the text does not match.
        return None


def parse_time(text):
    """Turns "14:30" (or "14:30:00") into a time object. None if it can't."""
    text = str(text).strip()
    try:
        return datetime.strptime(text[:5], "%H:%M").time()   # [:5] keeps "14:30"
    except ValueError:
        return None


def date_to_text(value):
    """Turns a date object back into "2026-11-20" ("" if there is no date)."""
    if value is None:
        return ""
    return value.strftime("%Y-%m-%d")


def time_to_text(value):
    """Turns a time object back into "14:30" ("" if there is no time)."""
    if value is None:
        return ""
    return value.strftime("%H:%M")
