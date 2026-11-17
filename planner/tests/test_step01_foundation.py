# Tests for Step 1: the foundation (home page, form helpers, the data models).

from datetime import date, time

from django.contrib.auth.models import User
from django.test import TestCase

from planner.form_tools import date_to_text, parse_date, parse_time, time_to_text
from planner.models import Course, Item, RepeatingEvent, Student


class FormToolsTests(TestCase):
    def test_parse_date(self):
        self.assertEqual(parse_date("2026-11-20"), date(2026, 11, 20))
        self.assertIsNone(parse_date(""))              # empty text
        self.assertIsNone(parse_date("next Friday"))   # nonsense text

    def test_parse_time(self):
        self.assertEqual(parse_time("14:30"), time(14, 30))
        self.assertEqual(parse_time("14:30:00"), time(14, 30))
        self.assertIsNone(parse_time(""))

    def test_back_to_text(self):
        self.assertEqual(date_to_text(date(2026, 11, 20)), "2026-11-20")
        self.assertEqual(time_to_text(time(9, 5)), "09:05")
        self.assertEqual(date_to_text(None), "")


class ModelSmokeTests(TestCase):
    # A "smoke test" just checks that the basics work at all:
    # can we save one of each model and read it back?

    def test_save_one_of_each_model(self):
        user = User.objects.create_user(username="sally@example.edu", email="sally@example.edu",
                                        password="password123", first_name="Sally")
        student = Student.objects.create(user=user)
        course = Course.objects.create(owner=student, name="Software Engineering", code="CS312")
        Item.objects.create(owner=student, course=course, title="Essay", due_date=date(2026, 11, 20))
        RepeatingEvent.objects.create(owner=student, title="Lecture", days_of_week="MON,THU")

        self.assertEqual(str(student), "Sally")
        self.assertEqual(course.count_items(), 1)
        self.assertEqual(len(student.get_items()), 1)
        self.assertEqual(len(student.get_events()), 1)


class HomePageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)    # 200 = OK
        self.assertContains(response, "Campus Hub")
