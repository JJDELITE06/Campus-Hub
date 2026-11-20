# planner/management/commands/seed_demo.py
#
# Fills the database with sample data so there is something to look at:
#       python manage.py seed_demo
#
# It creates two logins (both with the password  campushub123 ):
#       sally@example.edu   a student with classes, items and repeating events
#       jodi@example.edu    an administrator (can open the Admin page)
#
# It is safe to run more than once: it does nothing if Sally already exists.
# Notice that it builds the data with the SAME commands the web pages use.

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from planner.commands import (
    AddCourseCommand,
    AddItemCommand,
    AddRepeatingEventCommand,
    CommandInvoker,
    MarkCompleteCommand,
)
from planner.models import Student

PASSWORD = "campushub123"


class Command(BaseCommand):
    help = "Creates the demo users Sally (student) and Jodi (administrator)."

    def handle(self, *args, **options):
        if User.objects.filter(username="sally@example.edu").exists():
            self.stdout.write("Demo data is already there. Nothing to do.")
            return

        # ---- the two users ----
        sally_user = User.objects.create_user(
            username="sally@example.edu", email="sally@example.edu",
            password=PASSWORD, first_name="Sally",
        )
        sally = Student.objects.create(user=sally_user)
        User.objects.create_user(
            username="jodi@example.edu", email="jodi@example.edu",
            password=PASSWORD, first_name="Jodi", is_staff=True,
        )

        invoker = CommandInvoker({})
        today = date.today()

        def day(offset):
            """Returns the date "offset" days from today, as form text."""
            return (today + timedelta(days=offset)).strftime("%Y-%m-%d")

        # ---- classes and activities ----
        cs312 = AddCourseCommand(sally, {"name": "Software Engineering", "code": "CS312", "color": "#0d6efd"})
        calc = AddCourseCommand(sally, {"name": "Calculus II", "code": "MA152", "color": "#dc3545"})
        band = AddCourseCommand(sally, {"name": "Band", "color": "#198754", "is_activity": "on"})
        job = AddCourseCommand(sally, {"name": "Library work-study", "color": "#fd7e14", "is_activity": "on"})
        for command in [cs312, calc, band, job]:
            invoker.run(command)

        # ---- single items (the FACTORY picks the right creator for each type) ----
        forms = [
            {"title": "Problem set 7", "item_type": "ASSIGNMENT", "due_date": day(-1), "course_id": str(calc.course.pk)},
            {"title": "UML sequence diagrams", "item_type": "ASSIGNMENT", "due_date": day(0), "course_id": str(cs312.course.pk)},
            {"title": "Team 5 stand-up", "item_type": "MEETING", "due_date": day(1), "due_time": "16:00",
             "end_time": "16:30", "location": "Teams", "course_id": str(cs312.course.pk)},
            {"title": "Quiz 4: integration", "item_type": "TEST_QUIZ", "due_date": day(2), "due_time": "10:00",
             "location": "Room 210", "course_id": str(calc.course.pk)},
            {"title": "Library desk shift", "item_type": "JOB_SHIFT", "due_date": day(4), "due_time": "09:00",
             "end_time": "13:00", "location": "Main library", "course_id": str(job.course.pk)},
            {"title": "Final project presentation", "item_type": "PROJECT", "due_date": day(12),
             "notes": "Slides, demo and peer reviews.", "course_id": str(cs312.course.pk)},
            {"title": "Buy concert black shoes", "item_type": "OTHER", "due_date": day(6)},
            {"title": "Design patterns paper", "item_type": "ASSIGNMENT", "due_date": day(-5), "course_id": str(cs312.course.pk)},
        ]
        last_command = None
        for form in forms:
            last_command = AddItemCommand(sally, form)
            invoker.run(last_command)
        # Mark the last one (the paper) as already done.
        invoker.run(MarkCompleteCommand(sally, {"item_id": last_command.item.pk, "done": True}))

        # ---- repeating events ----
        invoker.run(AddRepeatingEventCommand(sally, {
            "title": "CS312 lecture", "item_type": "CLASS", "days_of_week": "MON,THU",
            "start_time": "09:30", "end_time": "10:45", "first_date": day(-60), "last_date": day(30),
            "location": "Room 104", "course_id": str(cs312.course.pk),
        }))
        invoker.run(AddRepeatingEventCommand(sally, {
            "title": "Band rehearsal", "item_type": "CLUB_MEETING", "days_of_week": "TUE",
            "start_time": "18:00", "end_time": "19:30", "first_date": day(-60), "last_date": day(30),
            "location": "Music hall", "course_id": str(band.course.pk),
        }))

        self.stdout.write("Done. Log in as sally@example.edu or jodi@example.edu, password: " + PASSWORD)
