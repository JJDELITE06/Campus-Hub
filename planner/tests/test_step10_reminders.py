# Tests for Step 10: the daily reminder email and its on/off switch (US-10, US-11).

from datetime import date

from django.core import mail
from django.core.management import call_command
from django.test import TestCase

from planner.models import Item, Student
from planner.services.daily_reminder_job import DailyReminderJob
from planner.services.email_service import EmailService

from .helpers import FakeEmailService, make_student

TODAY = date(2026, 11, 16)


class DailyReminderJobTests(TestCase):
    def setUp(self):
        self.sally = make_student()
        self.fake_email = FakeEmailService()
        self.job = DailyReminderJob(self.fake_email)      # inject the fake

    def test_email_lists_items_due_in_the_next_7_days_in_order(self):
        Item.objects.create(owner=self.sally, title="Later", due_date=date(2026, 11, 20))
        Item.objects.create(owner=self.sally, title="Sooner", due_date=date(2026, 11, 17))
        Item.objects.create(owner=self.sally, title="Too far away", due_date=date(2026, 12, 25))
        Item.objects.create(owner=self.sally, title="Already done", due_date=date(2026, 11, 17), completed=True)

        self.assertEqual(self.job.run(today=TODAY), 1)
        to, subject, body = self.fake_email.sent[0]
        self.assertEqual(to, "sally@example.edu")
        self.assertIn("Sooner", body)
        self.assertIn("Later", body)
        self.assertNotIn("Too far away", body)
        self.assertNotIn("Already done", body)
        # .index() gives the position of the text: smaller = earlier in the email.
        self.assertLess(body.index("Sooner"), body.index("Later"))
        self.assertIn("/login/", body)                    # the link to the app

    def test_hooray_email_when_nothing_is_due(self):
        self.job.run(today=TODAY)
        self.assertIn("Hooray, nothing is due", self.fake_email.sent[0][2])

    def test_no_email_when_reminders_are_off(self):
        self.sally.set_reminders(False)
        self.assertEqual(self.job.run(today=TODAY), 0)
        self.assertEqual(self.fake_email.sent, [])

    def test_each_email_only_has_that_students_items(self):
        carl = make_student(email="carl@example.edu", name="Carl")
        Item.objects.create(owner=self.sally, title="Sallys essay", due_date=date(2026, 11, 17))
        Item.objects.create(owner=carl, title="Carls lab", due_date=date(2026, 11, 17))
        self.job.run(today=TODAY)
        for to, subject, body in self.fake_email.sent:
            if to == "sally@example.edu":
                self.assertNotIn("Carls lab", body)
            else:
                self.assertNotIn("Sallys essay", body)

    def test_a_failed_send_is_not_counted(self):
        job = DailyReminderJob(FakeEmailService(works=False))
        self.assertEqual(job.run(today=TODAY), 0)


class EmailAndSettingsTests(TestCase):
    def test_email_service_sends_through_django(self):
        # During tests Django collects emails in mail.outbox instead of sending.
        self.assertTrue(EmailService().send("sally@example.edu", "Hi", "Hello"))
        self.assertEqual(mail.outbox[0].subject, "Hi")

    def test_manage_py_send_reminders(self):
        make_student()
        call_command("send_reminders")                    # same as typing it in the terminal
        self.assertEqual(len(mail.outbox), 1)

    def test_settings_page_switches_reminders_off_and_on(self):
        student = make_student()
        self.client.login(username="sally@example.edu", password="password123")
        self.client.post("/settings/", {})                              # switch off = nothing sent
        self.assertFalse(Student.objects.get(pk=student.pk).reminders_on)
        self.client.post("/settings/", {"reminders_on": "on"})
        self.assertTrue(Student.objects.get(pk=student.pk).reminders_on)
