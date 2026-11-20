# Tests for Step 4: the Item class, the Factory Method pattern and adding an item (US-05).

from datetime import date, time

from django.test import TestCase

from planner.commands import AddItemCommand, CommandInvoker
from planner.factories import AssignmentCreator, ItemCreator, all_creators, get_creator
from planner.models import Item, ItemType

from .helpers import make_student


class ItemTests(TestCase):
    def setUp(self):
        self.student = make_student()

    def test_validate_needs_title_and_date(self):
        item = Item(owner=self.student, title="", due_date=None)
        self.assertEqual(len(item.validate()), 2)       # two problems found

    def test_validate_end_time_must_be_after_start(self):
        item = Item(owner=self.student, title="Shift", due_date=date(2026, 11, 20),
                    due_time=time(14, 0), end_time=time(13, 0))
        self.assertEqual(item.validate(), ["The end time must be after the start time."])

    def test_update_only_changes_the_keys_it_is_given(self):
        item = Item(owner=self.student, title="Old", location="Room 1")
        item.update({"title": "New"})
        self.assertEqual(item.title, "New")
        self.assertEqual(item.location, "Room 1")       # untouched

    def test_is_overdue(self):
        item = Item(owner=self.student, title="Essay", due_date=date(2026, 11, 10))
        self.assertTrue(item.is_overdue(today=date(2026, 11, 11)))
        self.assertFalse(item.is_overdue(today=date(2026, 11, 10)))   # due today is not overdue
        item.completed = True
        self.assertFalse(item.is_overdue(today=date(2026, 11, 11)))   # done is never overdue


class FactoryTests(TestCase):
    def setUp(self):
        self.student = make_student()

    def test_abstract_creator_cannot_be_used_directly(self):
        # ItemCreator is abstract: Python raises TypeError if we try to make one.
        with self.assertRaises(TypeError):
            ItemCreator()

    def test_registry_finds_the_right_creator(self):
        creator = get_creator(ItemType.ASSIGNMENT)
        self.assertIsInstance(creator, AssignmentCreator)
        self.assertIsNone(get_creator("NO_SUCH_TYPE"))

    def test_assignment_defaults_to_1159_pm(self):
        creator = get_creator(ItemType.ASSIGNMENT)
        item = creator.create_item(self.student, {"title": "HW 1", "due_date": "2026-11-20", "due_time": ""})
        self.assertEqual(item.item_type, ItemType.ASSIGNMENT)
        self.assertEqual(item.due_time, time(23, 59))
        self.assertEqual(item.owner, self.student)

    def test_typed_time_beats_the_default(self):
        creator = get_creator(ItemType.ASSIGNMENT)
        item = creator.create_item(self.student, {"title": "HW 1", "due_date": "2026-11-20", "due_time": "09:00"})
        self.assertEqual(item.due_time, time(9, 0))

    def test_every_creator_makes_an_item_of_its_own_type(self):
        # This ONE test automatically covers any creator a teammate adds later.
        for creator in all_creators():
            item = creator.create_item(self.student, {"title": "Something", "due_date": "2026-11-20"})
            self.assertEqual(item.item_type, creator.type_code)
            self.assertNotEqual(creator.label, "")


class AddItemTests(TestCase):
    def setUp(self):
        self.student = make_student()
        self.invoker = CommandInvoker({})

    def test_add_item_saves_it(self):
        data = {"title": "Essay", "item_type": "ASSIGNMENT", "due_date": "2026-11-20"}
        self.assertTrue(self.invoker.run(AddItemCommand(self.student, data)))
        self.assertEqual(self.student.get_items()[0].title, "Essay")

    def test_add_item_with_errors_saves_nothing(self):
        data = {"title": "", "item_type": "ASSIGNMENT", "due_date": "not a date"}
        command = AddItemCommand(self.student, data)
        self.assertFalse(self.invoker.run(command))
        self.assertEqual(len(command.errors), 2)
        self.assertEqual(Item.objects.count(), 0)

    def test_add_item_with_unknown_type_fails(self):
        command = AddItemCommand(self.student, {"title": "X", "item_type": "BANANA", "due_date": "2026-11-20"})
        self.assertFalse(self.invoker.run(command))

    def test_add_item_page(self):
        self.client.login(username="sally@example.edu", password="password123")
        self.assertEqual(self.client.get("/items/add/").status_code, 200)
        response = self.client.post("/items/add/", {"title": "Lab 3", "item_type": "ASSIGNMENT",
                                                    "due_date": "2026-11-20", "due_time": "10:00"})
        self.assertRedirects(response, "/items/")
        self.assertContains(self.client.get("/items/"), "Lab 3")

    def test_home_sends_a_logged_in_student_to_the_list(self):
        self.client.login(username="sally@example.edu", password="password123")
        self.assertRedirects(self.client.get("/"), "/items/")

    def test_the_list_needs_a_login(self):
        # Nobody is logged in here, so we are sent to the login page.
        self.assertRedirects(self.client.get("/items/"), "/login/?next=/items/")

    def test_students_only_see_their_own_items(self):
        # US-02 / NFR-04
        carl = make_student(email="carl@example.edu", name="Carl")
        Item.objects.create(owner=carl, title="Carls secret item", due_date=date(2026, 11, 20))
        self.client.login(username="sally@example.edu", password="password123")
        self.assertNotContains(self.client.get("/items/"), "Carls secret item")
