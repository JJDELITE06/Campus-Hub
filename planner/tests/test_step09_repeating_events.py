# Tests for Step 9: repeating events (US-06, UC-04).

from datetime import date, time

from django.test import TestCase

from planner.commands import (
    AddRepeatingEventCommand,
    CommandInvoker,
    DeleteRepeatingEventCommand,
    EditRepeatingEventCommand,
)
from planner.models import RepeatingEvent
from planner.services.week_calendar import WeekCalendar

from .helpers import make_student

SUNDAY = date(2026, 11, 15)
MONDAY = date(2026, 11, 16)
THURSDAY = date(2026, 11, 19)

# A complete, valid form. Tests copy it and change one thing.
GOOD_FORM = {
    "title": "CS312 lecture", "item_type": "CLASS", "days_of_week": "MON,THU",
    "start_time": "09:30", "end_time": "10:45",
    "first_date": "2026-09-01", "last_date": "2026-12-15",
}


class RepeatingEventTests(TestCase):
    def setUp(self):
        self.student = make_student()
        self.invoker = CommandInvoker({})

    def add_event(self):
        command = AddRepeatingEventCommand(self.student, dict(GOOD_FORM))
        self.assertTrue(self.invoker.run(command))
        return command.event

    def test_add_event(self):
        event = self.add_event()
        self.assertEqual(event.get_days_list(), ["MON", "THU"])
        self.assertEqual(event.start_time, time(9, 30))

    def test_occurs_only_on_chosen_days_inside_the_range(self):
        event = self.add_event()
        self.assertTrue(event.occurs_on(MONDAY))
        self.assertTrue(event.occurs_on(THURSDAY))
        self.assertFalse(event.occurs_on(SUNDAY))                  # wrong day
        self.assertFalse(event.occurs_on(date(2026, 12, 17)))      # a Thursday after the last date

    def test_get_dates_in_week(self):
        event = self.add_event()
        self.assertEqual(event.get_dates_in_week(SUNDAY), [MONDAY, THURSDAY])

    def test_validation_errors(self):
        form = dict(GOOD_FORM)             # dict(...) makes a copy we can change
        form["days_of_week"] = ""
        form["end_time"] = "09:00"         # before the start time
        form["last_date"] = "2026-08-01"   # before the first date
        command = AddRepeatingEventCommand(self.student, form)
        self.assertFalse(self.invoker.run(command))
        self.assertEqual(len(command.errors), 3)
        self.assertEqual(RepeatingEvent.objects.count(), 0)

    def test_edit_changes_every_date(self):
        event = self.add_event()
        form = dict(GOOD_FORM)
        form["event_id"] = event.pk
        form["days_of_week"] = "TUE"
        self.assertTrue(self.invoker.run(EditRepeatingEventCommand(self.student, form)))
        event = RepeatingEvent.objects.get(pk=event.pk)
        self.assertFalse(event.occurs_on(MONDAY))
        self.assertTrue(event.occurs_on(date(2026, 11, 17)))       # a Tuesday

    def test_delete_just_one_date(self):
        event = self.add_event()
        data = {"event_id": event.pk, "only_date": "2026-11-19"}
        self.assertTrue(self.invoker.run(DeleteRepeatingEventCommand(self.student, data)))
        event = RepeatingEvent.objects.get(pk=event.pk)            # still exists
        self.assertFalse(event.occurs_on(THURSDAY))                # that one is gone
        self.assertTrue(event.occurs_on(MONDAY))                   # the others stay

    def test_delete_all_dates(self):
        event = self.add_event()
        self.invoker.run(DeleteRepeatingEventCommand(self.student, {"event_id": event.pk}))
        self.assertEqual(RepeatingEvent.objects.count(), 0)

    def test_events_show_on_the_calendar(self):
        self.add_event()
        calendar = WeekCalendar(self.student, SUNDAY)
        self.assertEqual(len(calendar.get_events_for(MONDAY)), 1)
        self.assertEqual(len(calendar.get_events_for(SUNDAY)), 0)
        self.assertFalse(calendar.is_empty())

    def test_event_pages(self):
        self.client.login(username="sally@example.edu", password="password123")
        self.assertEqual(self.client.get("/events/add/").status_code, 200)
        form = dict(GOOD_FORM)
        form["days"] = ["MON", "THU"]      # the page sends the days as checkboxes
        response = self.client.post("/events/add/", form)
        self.assertRedirects(response, "/calendar/")
        event = RepeatingEvent.objects.get()
        self.assertEqual(event.days_of_week, "MON,THU")
        self.assertContains(self.client.get("/calendar/?week=2026-11-15"), "CS312 lecture")
        self.assertContains(self.client.get("/events/" + str(event.pk) + "/?date=2026-11-19"), "Remove only")
        self.assertEqual(self.client.get("/events/" + str(event.pk) + "/edit/").status_code, 200)
