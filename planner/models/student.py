# planner/models/student.py -- the Student class (UML diagram CD-1).
#
# OUR UML SAYS:   User (abstract)  <|--  Student
#                 User (abstract)  <|--  Administrator
#
# HOW WE BUILT IT:
#   Django already comes with a tested "User" class that stores the name,
#   the email and the password HASH (a scrambled version of the password,
#   so the real password is never saved. That is requirement NFR-03).
#   Writing our own password code would be risky, so we REUSE Django's User.
#
#   Our Student class "HAS A" Django User (this is called COMPOSITION)
#   instead of "IS A" User (INHERITANCE). The Student adds the things only
#   students have, like the reminder email switch.
#
#   TRADEOFF: the code is a little different from the UML drawing, but we
#   get safe logins for free. This is a good thing to explain in the demo.

from datetime import date, timedelta

from django.contrib.auth.models import User   # Django's built-in user class
from django.db import models


class Student(models.Model):
    """One student who uses Campus Hub (the personas Sally and Carl)."""

    # ---------- attributes (these become columns in the database) ----------

    # OneToOneField = "each Student has exactly one User, and each User has
    # at most one Student".
    # on_delete=CASCADE = "if the User is deleted, delete this Student too".
    # related_name="student" lets us write   some_user.student
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student"
    )

    # UML: -remindersOn : Boolean = true   (US-11: the default is ON)
    reminders_on = models.BooleanField(default=True)

    # ---------- methods (UML CD-1) ----------

    def __str__(self):
        # __str__ decides what print(student) shows. Handy when debugging.
        return self.get_name()

    def get_name(self):
        """UML: +getName() : String"""
        # first_name is where we store the full name the student typed.
        # If it is empty we fall back to the email so we always show something.
        return self.user.first_name or self.user.email

    def get_email(self):
        """UML: +getEmail() : String"""
        return self.user.email

    def get_courses(self):
        """UML: +getCourses() : List<Course>  (classes AND activities)"""
        # "self.courses" exists because Course has related_name="courses".
        return list(self.courses.order_by("name"))

    def get_items(self):
        """UML: +getItems() : List<Item>  (sorted by due date, then time)"""
        return list(self.items.order_by("due_date", "due_time"))

    def get_events(self):
        """UML: +getEvents() : List<RepeatingEvent>"""
        return list(self.events.order_by("title"))

    def get_upcoming_items(self, days, today=None):
        """
        UML: +getUpcomingItems(days : int) : List<Item>

        Returns the NOT-done items that are due from today up to "days"
        days from now (and anything overdue, so nothing gets forgotten).

        "today" is an optional parameter. In real use we leave it out and
        the method asks the computer for today's date. In a UNIT TEST we
        pass a fixed date, so the test gives the same answer every day.
        """
        if today is None:
            today = date.today()
        last_day = today + timedelta(days=days)

        upcoming = []                      # start with an empty list
        for item in self.get_items():      # look at every item, in date order
            if not item.is_completed() and item.due_date <= last_day:
                upcoming.append(item)      # keep this one
        return upcoming

    def get_completed_items(self):
        """UML: +getCompletedItems() : List<Item>"""
        return list(self.items.filter(completed=True).order_by("due_date", "due_time"))

    def are_reminders_on(self):
        """UML: +areRemindersOn() : Boolean"""
        return self.reminders_on

    def set_reminders(self, on):
        """UML: +setReminders(on : Boolean) : void   (US-11)"""
        self.reminders_on = on
        self.save()    # save() writes the change to the database
