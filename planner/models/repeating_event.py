# planner/models/repeating_event.py -- the RepeatingEvent class (UML CD-2).
#
# A repeating event is something that happens every week on the same days,
# like a class on Monday and Thursday, or a job shift every Saturday (US-06).
#
# KEY DESIGN IDEA: we save ONE row that holds the RULE ("every MON and THU
# from Sep 1 to Dec 15"), NOT one row per date. The calendar asks the rule
# "do you happen on this day?".
#   + Saving a whole semester is instant (UC-04: 3 seconds or less).
#   + Changing the time changes every date at once.
#   - Changing just ONE date needs extra work (see skipped_dates below).

from datetime import timedelta

from django.db import models

from planner.form_tools import date_to_text, parse_date, parse_time, time_to_text

from .course import Course
from .item_type import ItemType
from .student import Student

# The day codes we store, in calendar order. Python's date.weekday() gives
# Monday=0 ... Sunday=6, so the position in this list matches that number.
DAY_CODES = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


class RepeatingEvent(models.Model):
    """A weekly repeating event such as a class, job shift or club meeting."""

    # ---------- attributes (UML CD-2) ----------
    title = models.CharField(max_length=200)
    item_type = models.CharField(max_length=20, default=ItemType.CLASS)

    # UML says daysOfWeek : List<String>. A database column can't hold a
    # Python list, so we store the text "MON,THU" and convert with
    # get_days_list() below. Simple, and easy to read in the admin page.
    days_of_week = models.CharField(max_length=40, default="")

    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    first_date = models.DateField(null=True)
    last_date = models.DateField(null=True)
    location = models.CharField(max_length=200, blank=True, default="")

    # Dates the student removed "just this one" from, stored as text like
    # "2026-11-26,2026-12-03" (UML: skippedDates : List<Date>).
    skipped_dates = models.TextField(blank=True, default="")

    owner = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="events")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="events", null=True, blank=True
    )

    # ---------- helper methods for the stored text lists ----------
    def __str__(self):
        return self.title

    def get_days_list(self):
        """Turns the stored text "MON,THU" into the list ["MON", "THU"]."""
        if self.days_of_week == "":
            return []
        return self.days_of_week.split(",")

    def get_skipped_list(self):
        """Turns the stored text into a list of real date objects."""
        dates = []
        for text in self.skipped_dates.split(","):
            one_date = parse_date(text)
            if one_date is not None:
                dates.append(one_date)
        return dates

    # ---------- methods (UML CD-2) ----------
    def validate(self):
        """UML: +validate() : List<String>   (empty list = all good)"""
        errors = []
        if self.title.strip() == "":
            errors.append("Please enter a title.")
        if len(self.get_days_list()) == 0:
            errors.append("Please pick at least one day of the week.")
        if self.start_time is None or self.end_time is None:
            errors.append("Please enter a start time and an end time.")
        elif self.end_time <= self.start_time:
            errors.append("The end time must be after the start time.")
        if self.first_date is None or self.last_date is None:
            errors.append("Please enter a first date and a last date.")
        elif self.last_date < self.first_date:
            errors.append("The last date must be on or after the first date.")
        return errors

    def occurs_on(self, day):
        """Does this event happen on this date? Returns True or False."""
        if self.first_date is None or self.last_date is None:
            return False
        if day < self.first_date or day > self.last_date:
            return False                                   # outside the date range
        if DAY_CODES[day.weekday()] not in self.get_days_list():
            return False                                   # wrong day of the week
        if day in self.get_skipped_list():
            return False                                   # the student skipped this one
        return True

    def get_dates_in_week(self, week_start):
        """UML: +getDatesInWeek(weekStart : Date) : List<Date>"""
        dates = []
        for number in range(7):                            # 0, 1, 2 ... 6
            day = week_start + timedelta(days=number)
            if self.occurs_on(day):
                dates.append(day)
        return dates

    def update_all(self, changes):
        """
        UML: +updateAll(changes : Map) : void
        Works like Item.update(): "changes" is a dictionary of form text, and
        only the keys that are present are changed. It does NOT save.
        """
        if "title" in changes:
            self.title = changes["title"].strip()
        if "item_type" in changes:
            self.item_type = changes["item_type"]
        if "days_of_week" in changes:
            self.days_of_week = changes["days_of_week"]
        if "start_time" in changes:
            self.start_time = parse_time(changes["start_time"])
        if "end_time" in changes:
            self.end_time = parse_time(changes["end_time"])
        if "first_date" in changes:
            self.first_date = parse_date(changes["first_date"])
        if "last_date" in changes:
            self.last_date = parse_date(changes["last_date"])
        if "location" in changes:
            self.location = changes["location"].strip()
        if "course_id" in changes:
            course_id = str(changes["course_id"])
            if course_id.isdigit():
                self.course = self.owner.courses.filter(pk=int(course_id)).first()
            else:
                self.course = None

    def to_form_data(self):
        """Returns this event as a dictionary of text, to fill the Edit form."""
        return {
            "title": self.title,
            "item_type": self.item_type,
            "days_of_week": self.days_of_week,
            "start_time": time_to_text(self.start_time),
            "end_time": time_to_text(self.end_time),
            "first_date": date_to_text(self.first_date),
            "last_date": date_to_text(self.last_date),
            "location": self.location,
            "course_id": str(self.course_id or ""),
        }

    def delete_one(self, day):
        """
        UML: +deleteOne(date : Date) : void
        Removes JUST ONE date by adding it to the skipped list.
        """
        skipped = self.get_skipped_list()
        if day not in skipped:
            skipped.append(day)
        # Turn the list of dates back into text: "2026-11-26,2026-12-03"
        texts = []
        for one_date in skipped:
            texts.append(date_to_text(one_date))
        self.skipped_dates = ",".join(texts)
        self.save()

    def delete_all(self):
        """UML: +deleteAll() : void   Removes the event from every date."""
        self.delete()

    def kind(self):
        """The creator for this event's type (label, icon, color)."""
        from planner.factories import get_creator_or_default
        return get_creator_or_default(self.item_type)
