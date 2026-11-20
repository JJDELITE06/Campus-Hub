# Tests for Step 5: the special rules of each item type.
# When you add a new creator, add a small test class for it here.

from django.test import TestCase

from planner.factories import get_creator
from planner.models import ItemType

from .helpers import make_student


class ItemTypeRuleTests(TestCase):
    def setUp(self):
        self.student = make_student()

    def errors_for(self, type_code, data):
        """A helper: builds an item with the factory and returns ALL its errors."""
        creator = get_creator(type_code)
        item = creator.create_item(self.student, data)
        return item.validate() + creator.extra_errors(item)

    def test_test_quiz_needs_a_time(self):
        errors = self.errors_for(ItemType.TEST_QUIZ, {"title": "Midterm", "due_date": "2026-11-20"})
        self.assertEqual(errors, ["A test or quiz needs a start time."])

    def test_meeting_needs_time_and_location(self):
        errors = self.errors_for(ItemType.MEETING, {"title": "Team 5", "due_date": "2026-11-20"})
        self.assertEqual(len(errors), 2)
        errors = self.errors_for(ItemType.MEETING, {"title": "Team 5", "due_date": "2026-11-20",
                                                    "due_time": "15:00", "location": "Teams"})
        self.assertEqual(errors, [])

    def test_job_shift_needs_start_and_end(self):
        errors = self.errors_for(ItemType.JOB_SHIFT, {"title": "Library desk", "due_date": "2026-11-20",
                                                      "due_time": "09:00"})
        self.assertEqual(errors, ["A job shift needs a start time and an end time."])

    def test_project_defaults_to_end_of_day(self):
        item = get_creator(ItemType.PROJECT).create_item(self.student, {"title": "Final", "due_date": "2026-12-02"})
        self.assertEqual(item.due_time.hour, 23)

    def test_other_has_no_extra_rules(self):
        errors = self.errors_for(ItemType.OTHER, {"title": "Laundry", "due_date": "2026-11-20"})
        self.assertEqual(errors, [])
