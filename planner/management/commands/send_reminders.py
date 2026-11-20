# planner/management/commands/send_reminders.py
#
# Adds a new job to manage.py:      python manage.py send_reminders
#
# NAME WARNING: Django calls these "management commands". They have nothing
# to do with our Command PATTERN in planner/commands/. Same word, two things.
# Django insists on this exact folder path and on a class named "Command".

from django.core.management.base import BaseCommand

from planner.services.daily_reminder_job import DailyReminderJob
from planner.services.email_service import EmailService


class Command(BaseCommand):
    help = "Sends the daily reminder email to every student who has it on."

    def handle(self, *args, **options):
        # Django calls handle() when the command is run.
        job = DailyReminderJob(EmailService())
        how_many = job.run()
        self.stdout.write("Sent " + str(how_many) + " reminder email(s).")
