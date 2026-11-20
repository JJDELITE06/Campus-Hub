# planner/models/course.py -- the Course class (UML diagram CD-2).
#
# A "Course" is a class (CS312) OR an activity (Debate Club, work-study job).
# The is_activity switch tells them apart. Items can be linked to a course so
# the student can filter "show me only CS312" (US-03).

from django.db import models

from .student import Student


class Course(models.Model):
    """A class or activity that belongs to one student."""

    # ---------- attributes ----------
    name = models.CharField(max_length=100)                    # "Software Engineering"
    code = models.CharField(max_length=20, blank=True, default="")   # "CS312" (optional)
    is_activity = models.BooleanField(default=False)           # False = class, True = activity

    # A color makes classes easy to tell apart on the list and the calendar.
    # It is stored as a web color code such as "#0d6efd" (blue).
    # (Not in UML CD-2 yet: it comes from our requirements idea FR-04.)
    color = models.CharField(max_length=7, default="#0d6efd")

    # ForeignKey = "many courses belong to one student".
    # related_name="courses" lets us write   student.courses
    owner = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="courses")

    # ---------- methods ----------
    def __str__(self):
        return self.get_name()

    def get_name(self):
        """UML: +getName() : String   e.g. "CS312 - Software Engineering" """
        if self.code:
            return self.code + " - " + self.name
        return self.name

    def get_items(self):
        """UML: +getItems() : List<Item>"""
        # "self.items" exists because Item.course has related_name="items".
        return list(self.items.order_by("due_date", "due_time"))

    def count_items(self):
        """UML: +countItems() : int"""
        return self.items.count()

    def rename(self, name, code):
        """UML: +rename(name : String, code : String) : void"""
        self.name = name.strip()
        self.code = code.strip()
        self.save()

    def validate(self):
        """
        Checks the course BEFORE saving. Returns a list of error messages.
        An EMPTY list means "everything is fine".
        """
        errors = []
        if self.name.strip() == "":
            errors.append("Please enter a name for the class or activity.")
        return errors

    def delete_with_items(self):
        """
        UML: +deleteWithItems() : int      (UC-10 Drop a class)

        Deletes this course AND everything linked to it.
        Returns how many items were deleted, so the page can say
        "CS312 and its 4 items were deleted".
        """
        how_many = self.count_items()
        # Because Item.course uses on_delete=CASCADE, deleting the course
        # automatically deletes its items and repeating events too.
        self.delete()
        return how_many
