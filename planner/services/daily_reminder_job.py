# planner/services/daily_reminder_job.py -- DailyReminderJob (UML CD-4).
#
# Sends every student with reminders ON one email listing what is due in the
# next 7 days (US-10, UC-14, SD-14).
#
# HOW IT IS STARTED:  python manage.py send_reminders
# On a real server, a scheduler runs that command every morning at 6:30 AM.
#
# THE EMAIL SERVICE IS PASSED IN (this is called "dependency injection").
# In real use we pass a real EmailService. In a unit test we pass a FAKE one
# that just remembers what it was asked to send. The job can't tell the
# difference, so we can test it without sending any email.

import logging
from datetime import date

from django.conf import settings

from planner.models import Student

# A logger writes messages for developers (shown in the terminal).
logger = logging.getLogger(__name__)

DAYS_AHEAD = 7     # US-10: "everything due this week"


class DailyReminderJob:
    """Builds and sends the daily reminder emails."""

    def __init__(self, email_service):
        self.email_service = email_service     # UML: -emailService : EmailService

    def run(self, today=None):
        """
        UML: +run() : void
        Returns how many emails were sent (handy for tests and the terminal).
        """
        if today is None:
            today = date.today()

        sent = 0
        # Only students who have reminders turned ON (US-11).
        for student in Student.objects.filter(reminders_on=True):
            items = self.build_list(student, today)
            body = self.write_email(student, items, today)
            subject = "Campus Hub: " + str(len(items)) + " item(s) coming up"
            if self.email_service.send(student.get_email(), subject, body):
                sent = sent + 1
            else:
                self.log_error(student, "the email could not be sent")
        return sent

    # In the UML the next three methods are private (-). Python has no real
    # "private", and we want to unit test them, so we leave them public.

    def build_list(self, student, today):
        """UML: -buildList(student : Student) : List<Item>"""
        # The Student already knows how to do this, so we just ask it.
        # The list contains ONLY this student's items (UC-14).
        return student.get_upcoming_items(DAYS_AHEAD, today)

    def write_email(self, student, items, today):
        """UML: -writeEmail(student : Student, items : List<Item>) : String"""
        lines = []
        lines.append("Hi " + student.get_name() + ",")
        lines.append("")

        if len(items) == 0:
            # US-10 acceptance criterion 4.
            lines.append("Hooray, nothing is due in the next 7 days!")
        else:
            lines.append("Here is what is coming up in the next 7 days:")
            lines.append("")
            for item in items:
                when = item.due_date.strftime("%a %b %d")       # "Fri Nov 20"
                if item.due_time is not None:
                    when = when + " at " + item.due_time.strftime("%I:%M %p")
                line = "  - " + when + " | " + item.kind().label + " | " + item.title
                if item.is_overdue(today):
                    line = line + "  (OVERDUE)"
                lines.append(line)

        lines.append("")
        lines.append("Open Campus Hub: " + settings.SITE_URL)
        lines.append("")
        lines.append("You can turn these emails off on the Settings page.")
        # "\n" is the "new line" character. join() glues the lines together.
        return "\n".join(lines)

    def log_error(self, student, message):
        """UML: -logError(student : Student, message : String) : void"""
        logger.error("Reminder for %s failed: %s", student.get_email(), message)
