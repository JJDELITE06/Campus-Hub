# Tests for Step 2: accounts (US-01, US-02).

from django.contrib.auth.models import User
from django.test import TestCase

from planner.models import Student

from .helpers import make_student


class StudentTests(TestCase):
    def test_new_student_has_reminders_on(self):
        # US-11: the default for new users is ON.
        student = make_student()
        self.assertTrue(student.are_reminders_on())

    def test_set_reminders_saves_the_change(self):
        student = make_student()
        student.set_reminders(False)
        # Read the student from the database again to prove it was SAVED.
        fresh = Student.objects.get(pk=student.pk)
        self.assertFalse(fresh.are_reminders_on())

    def test_get_name_and_email(self):
        student = make_student(email="carl@example.edu", name="Carl")
        self.assertEqual(student.get_name(), "Carl")
        self.assertEqual(student.get_email(), "carl@example.edu")


class AccountPageTests(TestCase):
    # self.client is a pretend web browser that Django gives every TestCase.

    def test_sign_up_creates_account_and_logs_in(self):
        response = self.client.post("/signup/", {
            "name": "Sally", "email": "sally@example.edu",
            "password": "password123", "password_again": "password123",
        })
        # 302 = "go to another page". We are sent to the home page "/".
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        self.assertEqual(Student.objects.count(), 1)

    def test_password_is_not_stored_as_plain_text(self):
        # NFR-03: passwords are stored only as hashes.
        make_student(password="password123")
        user = User.objects.get(username="sally@example.edu")
        self.assertNotEqual(user.password, "password123")

    def test_sign_up_rejects_an_email_that_is_already_used(self):
        make_student(email="sally@example.edu")
        response = self.client.post("/signup/", {
            "name": "Other Sally", "email": "sally@example.edu",
            "password": "password123", "password_again": "password123",
        })
        self.assertContains(response, "already exists")
        self.assertEqual(Student.objects.count(), 1)    # still only one

    def test_sign_up_rejects_short_and_mismatched_passwords(self):
        response = self.client.post("/signup/", {
            "name": "Sally", "email": "sally@example.edu",
            "password": "short", "password_again": "short",
        })
        self.assertContains(response, "at least 8 characters")
        response = self.client.post("/signup/", {
            "name": "Sally", "email": "sally@example.edu",
            "password": "password123", "password_again": "different123",
        })
        self.assertContains(response, "do not match")

    def test_log_in_with_wrong_password_shows_error(self):
        make_student()
        response = self.client.post("/login/", {"email": "sally@example.edu", "password": "wrong"})
        self.assertContains(response, "Email or password is incorrect")

    def test_log_in_then_log_out(self):
        make_student()
        response = self.client.post("/login/", {"email": "sally@example.edu", "password": "password123"})
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        # While logged in, the session (the browser's notebook) holds our user id.
        self.assertIn("_auth_user_id", self.client.session)
        self.client.post("/logout/")
        # After logging out, it is gone.
        self.assertNotIn("_auth_user_id", self.client.session)
