# Tests for Step 7: the ItemFilter class (US-03, US-09).
# ItemFilter is plain Python, so these tests do not even need saved items.

from datetime import date

from django.test import TestCase

from planner.models import Course, Item
from planner.services.item_filter import ItemFilter

from .helpers import make_student


class ItemFilterTests(TestCase):
    def setUp(self):
        self.student = make_student()
        self.cs312 = Course.objects.create(owner=self.student, name="Software Engineering", code="CS312")
        self.band = Course.objects.create(owner=self.student, name="Band", is_activity=True)
        day = date(2026, 11, 20)
        self.items = [
            Item(owner=self.student, title="UML homework", item_type="ASSIGNMENT", course=self.cs312, due_date=day),
            Item(owner=self.student, title="Midterm", item_type="TEST_QUIZ", course=self.cs312, due_date=day),
            Item(owner=self.student, title="Rehearsal", item_type="CLUB_MEETING", course=self.band, due_date=day),
            Item(owner=self.student, title="Old quiz", item_type="TEST_QUIZ", due_date=day, completed=True),
        ]

    def titles(self, items):
        """A helper: turns a list of items into a list of their titles."""
        result = []
        for item in items:
            result.append(item.title)
        return result

    def test_no_filter_shows_everything(self):
        self.assertEqual(len(ItemFilter().apply(self.items)), 4)

    def test_filter_by_course(self):
        item_filter = ItemFilter()
        item_filter.set_course(self.cs312)
        self.assertEqual(self.titles(item_filter.apply(self.items)), ["UML homework", "Midterm"])

    def test_filter_by_type(self):
        item_filter = ItemFilter()
        item_filter.set_type("TEST_QUIZ")
        self.assertEqual(self.titles(item_filter.apply(self.items)), ["Midterm", "Old quiz"])

    def test_both_filters_together(self):
        item_filter = ItemFilter()
        item_filter.set_course(self.cs312)
        item_filter.set_type("TEST_QUIZ")
        self.assertEqual(self.titles(item_filter.apply(self.items)), ["Midterm"])

    def test_hide_completed(self):
        item_filter = ItemFilter()
        item_filter.show_completed = False
        self.assertEqual(len(item_filter.apply(self.items)), 3)

    def test_clear_goes_back_to_all(self):
        item_filter = ItemFilter()
        item_filter.set_type("TEST_QUIZ")
        self.assertTrue(item_filter.is_active())
        item_filter.clear()
        self.assertFalse(item_filter.is_active())
        self.assertEqual(len(item_filter.apply(self.items)), 4)

    def test_filter_on_the_page(self):
        for item in self.items:
            item.save()
        self.client.login(username="sally@example.edu", password="password123")
        response = self.client.get("/items/?type=CLUB_MEETING")
        self.assertContains(response, "Rehearsal")
        self.assertNotContains(response, "UML homework")
