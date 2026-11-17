# Tests for Step 3: classes and activities (UC-09, UC-10).

from datetime import date

from django.test import TestCase

from planner.commands import AddCourseCommand, CommandInvoker, DropCourseCommand
from planner.models import Course, Item

from .helpers import make_student


class CourseTests(TestCase):
    def setUp(self):
        # setUp() runs before EVERY test in this class.
        self.student = make_student()
        self.invoker = CommandInvoker({})    # a plain dict is the "memory"

    def test_get_name_with_and_without_code(self):
        with_code = Course(name="Software Engineering", code="CS312")
        without_code = Course(name="Debate Club")
        self.assertEqual(with_code.get_name(), "CS312 - Software Engineering")
        self.assertEqual(without_code.get_name(), "Debate Club")

    def test_add_course_command(self):
        command = AddCourseCommand(self.student, {"name": "Software Engineering", "code": "CS312"})
        self.assertTrue(self.invoker.run(command))
        self.assertEqual(len(self.student.get_courses()), 1)

    def test_add_course_needs_a_name(self):
        command = AddCourseCommand(self.student, {"name": "   "})
        self.assertFalse(self.invoker.run(command))
        self.assertEqual(Course.objects.count(), 0)     # nothing was saved

    def test_drop_course_deletes_its_items_too(self):
        course = Course.objects.create(owner=self.student, name="Calculus")
        Item.objects.create(owner=self.student, course=course, title="HW 1", due_date=date(2026, 11, 20))
        Item.objects.create(owner=self.student, course=course, title="HW 2", due_date=date(2026, 11, 27))
        Item.objects.create(owner=self.student, title="No class item", due_date=date(2026, 11, 27))

        command = DropCourseCommand(self.student, {"course_id": course.pk})
        self.assertTrue(self.invoker.run(command))

        self.assertEqual(command.deleted_count, 2)
        self.assertEqual(Course.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 1)       # the other item is safe

    def test_cannot_drop_another_students_course(self):
        # NFR-04: no student can change another student's data.
        other = make_student(email="carl@example.edu", name="Carl")
        carls_course = Course.objects.create(owner=other, name="Physics")
        command = DropCourseCommand(self.student, {"course_id": carls_course.pk})
        self.assertFalse(self.invoker.run(command))
        self.assertEqual(Course.objects.count(), 1)

    def test_course_pages_load(self):
        self.client.login(username="sally@example.edu", password="password123")
        self.assertEqual(self.client.get("/courses/").status_code, 200)   # 200 = OK
        response = self.client.post("/courses/add/", {"name": "Band", "is_activity": "on", "color": "#ff0000"})
        self.assertRedirects(response, "/courses/")
        self.assertTrue(Course.objects.get(name="Band").is_activity)
