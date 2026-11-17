# Tests for Step 8: the WeekCalendar class (US-13, UC-13).

from datetime import date

from django.test import TestCase

from planner.models import Item
from planner.services.week_calendar import WeekCalendar, start_of_week

from .helpers import make_student

# Handy fixed dates. Nov 15 2026 is a Sunday, Nov 18 is the Wednesday after.
SUNDAY = date(2026, 11, 15)
WEDNESDAY = date(2026, 11, 18)


class WeekCalendarTests(TestCase):
    def setUp(self):
        self.student = make_student()

    def test_week_starts_on_sunday(self):
        self.assertEqual(start_of_week(WEDNESDAY), SUNDAY)
        self.assertEqual(start_of_week(SUNDAY), SUNDAY)
        self.assertEqual(start_of_week(date(2026, 11, 21)), SUNDAY)     # Saturday

    def test_week_has_seven_days(self):
        days = WeekCalendar(self.student, WEDNESDAY).get_days()
        self.assertEqual(len(days), 7)
        self.assertEqual(days[0], SUNDAY)
        self.assertEqual(days[6], date(2026, 11, 21))

    def test_next_and_previous_week(self):
        calendar = WeekCalendar(self.student, WEDNESDAY)
        calendar.next_week()
        self.assertEqual(calendar.week_start, date(2026, 11, 22))
        calendar.previous_week()
        calendar.previous_week()
        self.assertEqual(calendar.week_start, date(2026, 11, 8))

    def test_items_show_on_their_due_day_only(self):
        Item.objects.create(owner=self.student, title="Essay", due_date=WEDNESDAY)
        calendar = WeekCalendar(self.student, WEDNESDAY)
        self.assertEqual(len(calendar.get_items_for(WEDNESDAY)), 1)
        self.assertEqual(len(calendar.get_items_for(SUNDAY)), 0)

    def test_is_empty(self):
        calendar = WeekCalendar(self.student, WEDNESDAY)
        self.assertTrue(calendar.is_empty())
        Item.objects.create(owner=self.student, title="Essay", due_date=WEDNESDAY)
        self.assertFalse(calendar.is_empty())

    def test_calendar_page(self):
        Item.objects.create(owner=self.student, title="Essay", due_date=WEDNESDAY)
        self.client.login(username="sally@example.edu", password="password123")
        self.assertContains(self.client.get("/calendar/?week=2026-11-18"), "Essay")
        self.assertContains(self.client.get("/calendar/?week=2026-11-25"), "Nothing due this week")
