# planner/services/week_calendar.py -- the WeekCalendar class (UML CD-3).
#
# Works out what is on each day of one week (US-13, UC-13).
# The calendar only LOOKS at data. It never changes anything.

from datetime import date, timedelta


def start_of_week(day):
    """
    Returns the SUNDAY of the week that contains "day" (UC-13 says the week
    runs Sunday to Saturday).

    Python's weekday() gives Monday=0 ... Sunday=6. Adding 1 and taking the
    remainder after dividing by 7 (the % operator) turns that into
    "how many days since Sunday": Sunday=0, Monday=1 ... Saturday=6.
    """
    days_since_sunday = (day.weekday() + 1) % 7
    return day - timedelta(days=days_since_sunday)


class WeekCalendar:
    """One week of a student's planner."""

    def __init__(self, student, week_start=None):
        self.student = student                         # UML: -student : Student
        if week_start is None:
            week_start = date.today()
        # Whatever day we are given, snap back to that week's Sunday.
        self.week_start = start_of_week(week_start)    # UML: -weekStart : Date

    def next_week(self):
        """UML: +nextWeek() : void"""
        self.week_start = self.week_start + timedelta(days=7)

    def previous_week(self):
        """UML: +previousWeek() : void"""
        self.week_start = self.week_start - timedelta(days=7)

    def get_days(self):
        """Returns the 7 dates of this week, Sunday first."""
        days = []
        for number in range(7):
            days.append(self.week_start + timedelta(days=number))
        return days

    def get_items_for(self, day):
        """UML: +getItemsFor(day : Date) : List<Item>"""
        return list(self.student.items.filter(due_date=day).order_by("due_time"))

    def get_events_for(self, day):
        """UML: +getEventsFor(day : Date) : List<RepeatingEvent>"""
        events = []
        for event in self.student.events.order_by("start_time"):
            if event.occurs_on(day):
                events.append(event)
        return events

    def is_empty(self):
        """UML: +isEmpty() : Boolean   True when nothing is on this week."""
        for day in self.get_days():
            if self.get_items_for(day) or self.get_events_for(day):
                return False
        return True
