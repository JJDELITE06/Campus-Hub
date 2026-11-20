# planner/models/item.py -- the Item class (UML diagram CD-2).
#
# An Item is ONE thing on the planner: an assignment, a quiz, a meeting,
# a job shift... The "item_type" attribute says which kind it is.
#
# This class only knows the things that are true for EVERY item.
# The things that are different for each type (label, icon, special rules)
# live in the FACTORY classes: see planner/factories/base.py.

from datetime import date

from django.db import models

from planner.form_tools import date_to_text, parse_date, parse_time, time_to_text

from .course import Course
from .item_type import ItemType
from .student import Student


class Item(models.Model):
    """One entry in a student's planner."""

    # ---------- attributes (UML CD-2) ----------
    title = models.CharField(max_length=200)
    item_type = models.CharField(max_length=20, default=ItemType.OTHER)
    due_date = models.DateField(null=True)                  # the day it is due / happens
    due_time = models.TimeField(null=True, blank=True)      # the time (optional)
    # end_time is for things with a length, like a meeting or a job shift.
    # (Not in UML CD-2 yet. Added for meetings and shifts.)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    completed = models.BooleanField(default=False)

    # Each item belongs to exactly one student (requirement NFR-04:
    # nobody can see another student's items).
    owner = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="items")

    # The course is OPTIONAL (null=True): an item can have no class.
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="items", null=True, blank=True
    )

    # ---------- methods (UML CD-2) ----------
    def __str__(self):
        return self.title

    def validate(self):
        """
        UML: +validate() : List<String>

        Checks the rules that are the same for EVERY type of item.
        Returns a list of error messages. An empty list means "all good".
        (Type-specific rules are added by the factory: see extra_errors().)
        """
        errors = []
        if self.title.strip() == "":
            errors.append("Please enter a title.")
        if self.due_date is None:
            errors.append("Please enter a valid date.")
        if self.due_time and self.end_time and self.end_time <= self.due_time:
            errors.append("The end time must be after the start time.")
        return errors

    def update(self, changes):
        """
        UML: +update(changes : Map) : void

        "changes" is a DICTIONARY of text values, exactly as a web form
        sends them, for example:
            {"title": "Essay", "due_date": "2026-11-20", "due_time": "23:59"}

        RULE: only the keys that are IN the dictionary are changed.
        A key that is missing is left alone. This does NOT save to the
        database. The caller validates first and then calls save().
        """
        if "title" in changes:
            self.title = changes["title"].strip()
        if "item_type" in changes:
            self.item_type = changes["item_type"]
        if "due_date" in changes:
            self.due_date = parse_date(changes["due_date"])
        if "due_time" in changes:
            self.due_time = parse_time(changes["due_time"])
        if "end_time" in changes:
            self.end_time = parse_time(changes["end_time"])
        if "location" in changes:
            self.location = changes["location"].strip()
        if "notes" in changes:
            self.notes = changes["notes"].strip()
        if "course_id" in changes:
            # Look for the course ONLY among this student's own courses.
            # .first() gives the course, or None when nothing matches.
            course_id = str(changes["course_id"])
            if course_id.isdigit():
                self.course = self.owner.courses.filter(pk=int(course_id)).first()
            else:
                self.course = None

    def to_form_data(self):
        """
        The opposite of update(): returns this item as a dictionary of text.
        We use it to fill in the Edit form, and the Command pattern uses it
        to take a "photo" of an item so a change can be undone later.
        """
        return {
            "title": self.title,
            "item_type": self.item_type,
            "due_date": date_to_text(self.due_date),
            "due_time": time_to_text(self.due_time),
            "end_time": time_to_text(self.end_time),
            "location": self.location,
            "notes": self.notes,
            "course_id": str(self.course_id or ""),
        }

    def mark_complete(self):
        """UML: +markComplete() : void   (US-08)"""
        self.completed = True
        self.save()

    def mark_not_done(self):
        """UML: +markNotDone() : void"""
        self.completed = False
        self.save()

    def is_completed(self):
        """UML: +isCompleted() : Boolean"""
        return self.completed

    def is_overdue(self, today=None):
        """
        UML: +isOverdue(today : Date) : Boolean

        An item is overdue when it is NOT done and its date is before today.
        Templates call this with no argument, tests pass a fixed date.
        """
        if today is None:
            today = date.today()
        return (not self.completed) and self.due_date is not None and self.due_date < today

    # UML also lists +delete() : void. We do not write it ourselves:
    # every Django model INHERITS a delete() method from models.Model.

    # ---------- display helpers used by the web pages ----------
    def kind(self):
        """
        Returns the "creator" object for this item's type. The creator knows
        the label, icon and color to show (see planner/factories/).

        The import is INSIDE the method on purpose. The factories import
        Item, so if Item imported the factories at the top of the file,
        Python would go round in a circle (a "circular import").
        """
        from planner.factories import get_creator_or_default
        return get_creator_or_default(self.item_type)
