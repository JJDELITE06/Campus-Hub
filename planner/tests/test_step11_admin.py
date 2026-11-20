# Tests for Step 11: the administrator deletes a student (US-12, UC-16).

from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from planner.models import Administrator, Course, Item, Student

from .helpers import make_student


class AdministratorTests(TestCase):
    def setUp(self):
        # is_staff=True is what makes a user an administrator.
        self.jodi_user = User.objects.create_user(
            username="jodi@example.edu", email="jodi@example.edu",
            password="password123", first_name="Jodi", is_staff=True,
        )
        self.administrator = Administrator(self.jodi_user)
        self.sally = make_student()
        self.carl = make_student(email="carl@example.edu", name="Carl")

    def test_list_and_search(self):
        self.assertEqual(len(self.administrator.list_students()), 2)
        self.assertEqual(self.administrator.search_students("carl"), [self.carl])
        self.assertEqual(self.administrator.search_students("SALLY"), [self.sally])   # ignores case
        self.assertEqual(len(self.administrator.search_students("")), 2)

    def test_delete_student_removes_all_their_data(self):
        course = Course.objects.create(owner=self.sally, name="Calculus")
        Item.objects.create(owner=self.sally, course=course, title="HW", due_date=date(2026, 11, 20))
        self.administrator.delete_student(self.sally)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Course.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
        self.assertFalse(User.objects.filter(username="sally@example.edu").exists())

    def test_deleted_student_can_sign_up_again(self):
        # US-12 acceptance criterion 6.
        self.administrator.delete_student(self.sally)
        response = self.client.post("/signup/", {
            "name": "Sally", "email": "sally@example.edu",
            "password": "password123", "password_again": "password123",
        })
        self.assertRedirects(response, "/", fetch_redirect_response=False)

    def test_students_cannot_open_the_admin_pages(self):
        self.client.login(username="sally@example.edu", password="password123")
        response = self.client.get("/manage/students/")
        self.assertEqual(response.status_code, 302)      # 302 = sent somewhere else (login)

    def test_admin_pages(self):
        self.client.login(username="jodi@example.edu", password="password123")
        self.assertContains(self.client.get("/manage/students/"), "carl@example.edu")
        self.assertNotContains(self.client.get("/manage/students/?search=sally"), "carl@example.edu")
        url = "/manage/students/" + str(self.carl.pk) + "/delete/"
        self.assertContains(self.client.get(url), "Are you sure?")
        self.client.post(url)
        self.assertEqual(Student.objects.count(), 1)
