# Tests for Step 6: the Command pattern: edit, delete, complete, delete many, undo
# (US-04, US-07, US-08, UC-08).

from datetime import date

from django.test import TestCase

from planner.commands import (
    AddItemCommand,
    Command,
    CommandInvoker,
    DeleteItemCommand,
    DeleteSelectedCommand,
    EditItemCommand,
    MarkCompleteCommand,
)
from planner.models import Item

from .helpers import make_student


class CommandTests(TestCase):
    def setUp(self):
        self.student = make_student()
        self.memory = {}                           # stands in for the session
        self.invoker = CommandInvoker(self.memory)
        self.item = Item.objects.create(owner=self.student, title="Essay",
                                        item_type="ASSIGNMENT", due_date=date(2026, 11, 20))

    def reload(self):
        """Reads self.item again from the database."""
        return Item.objects.get(pk=self.item.pk)

    def test_abstract_command_cannot_be_used_directly(self):
        with self.assertRaises(TypeError):
            Command(self.student, {})

    # ---- edit ----
    def test_edit_then_undo(self):
        data = {"item_id": self.item.pk, "title": "Essay v2", "due_date": "2026-11-25"}
        self.assertTrue(self.invoker.run(EditItemCommand(self.student, data)))
        self.assertEqual(self.reload().title, "Essay v2")
        self.assertEqual(self.reload().due_date, date(2026, 11, 25))

        self.invoker.undo_last(self.student)
        self.assertEqual(self.reload().title, "Essay")
        self.assertEqual(self.reload().due_date, date(2026, 11, 20))

    def test_edit_with_errors_changes_nothing(self):
        data = {"item_id": self.item.pk, "title": ""}
        command = EditItemCommand(self.student, data)
        self.assertFalse(self.invoker.run(command))
        self.assertEqual(self.reload().title, "Essay")

    # ---- delete ----
    def test_delete_then_undo_brings_it_back(self):
        self.assertTrue(self.invoker.run(DeleteItemCommand(self.student, {"item_id": self.item.pk})))
        self.assertEqual(Item.objects.count(), 0)

        self.invoker.undo_last(self.student)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().title, "Essay")

    def test_cannot_delete_another_students_item(self):
        carl = make_student(email="carl@example.edu", name="Carl")
        command = DeleteItemCommand(carl, {"item_id": self.item.pk})
        self.assertFalse(CommandInvoker({}).run(command))
        self.assertEqual(Item.objects.count(), 1)

    # ---- complete ----
    def test_mark_complete_and_not_done(self):
        self.invoker.run(MarkCompleteCommand(self.student, {"item_id": self.item.pk, "done": True}))
        self.assertTrue(self.reload().is_completed())
        self.assertEqual(len(self.student.get_completed_items()), 1)

        self.invoker.run(MarkCompleteCommand(self.student, {"item_id": self.item.pk, "done": False}))
        self.assertFalse(self.reload().is_completed())

    def test_undo_mark_complete(self):
        self.invoker.run(MarkCompleteCommand(self.student, {"item_id": self.item.pk, "done": True}))
        self.invoker.undo_last(self.student)
        self.assertFalse(self.reload().is_completed())

    # ---- delete many ----
    def test_delete_selected_and_undo(self):
        second = Item.objects.create(owner=self.student, title="Quiz", due_date=date(2026, 11, 21))
        third = Item.objects.create(owner=self.student, title="Keep me", due_date=date(2026, 11, 22))
        command = DeleteSelectedCommand(self.student, {"item_ids": [self.item.pk, second.pk]})
        self.assertTrue(self.invoker.run(command))
        self.assertEqual(command.deleted_count, 2)
        self.assertEqual(Item.objects.count(), 1)

        self.invoker.undo_last(self.student)
        self.assertEqual(Item.objects.count(), 3)

    def test_delete_selected_with_nothing_selected(self):
        command = DeleteSelectedCommand(self.student, {"item_ids": []})
        self.assertFalse(self.invoker.run(command))

    # ---- the invoker ----
    def test_undo_add(self):
        data = {"title": "Lab", "item_type": "ASSIGNMENT", "due_date": "2026-11-20"}
        self.invoker.run(AddItemCommand(self.student, data))
        self.assertEqual(Item.objects.count(), 2)
        self.invoker.undo_last(self.student)
        self.assertEqual(Item.objects.count(), 1)

    def test_undo_only_works_once(self):
        self.invoker.run(DeleteItemCommand(self.student, {"item_id": self.item.pk}))
        self.assertIsNotNone(self.invoker.undo_last(self.student))
        self.assertIsNone(self.invoker.undo_last(self.student))     # nothing left

    def test_undo_with_nothing_to_undo(self):
        self.assertIsNone(self.invoker.undo_last(self.student))


class CommandPageTests(TestCase):
    def setUp(self):
        self.student = make_student()
        self.client.login(username="sally@example.edu", password="password123")
        self.item = Item.objects.create(owner=self.student, title="Essay",
                                        item_type="ASSIGNMENT", due_date=date(2026, 11, 20))

    def test_edit_page_saves(self):
        url = "/items/" + str(self.item.pk) + "/edit/"
        self.assertContains(self.client.get(url), "Essay")
        self.client.post(url, {"title": "Essay final", "item_type": "ASSIGNMENT", "due_date": "2026-11-20"})
        self.assertEqual(Item.objects.get(pk=self.item.pk).title, "Essay final")

    def test_delete_asks_first_then_deletes_then_undo(self):
        url = "/items/" + str(self.item.pk) + "/delete/"
        self.assertContains(self.client.get(url), "Do you really want to delete this?")
        self.assertEqual(Item.objects.count(), 1)       # GET did not delete
        self.client.post(url)
        self.assertEqual(Item.objects.count(), 0)
        self.client.post("/undo/")                      # the Undo button
        self.assertEqual(Item.objects.count(), 1)

    def test_complete_button(self):
        self.client.post("/items/" + str(self.item.pk) + "/complete/", {"done": "1"})
        self.assertTrue(Item.objects.get(pk=self.item.pk).completed)

    def test_delete_selected_page(self):
        self.client.post("/items/delete-selected/", {"item_ids": [str(self.item.pk)]})
        self.assertEqual(Item.objects.count(), 0)

    def test_cannot_open_another_students_item(self):
        carl = make_student(email="carl@example.edu", name="Carl")
        carls = Item.objects.create(owner=carl, title="Carls", due_date=date(2026, 11, 20))
        response = self.client.get("/items/" + str(carls.pk) + "/edit/")
        self.assertEqual(response.status_code, 404)     # 404 = Not Found
