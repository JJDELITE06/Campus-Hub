# planner/services/email_service.py -- the EmailService class (UML CD-4).
#
# A thin wrapper around Django's email function. Everything in Campus Hub
# that sends email goes through this ONE class, so if we change email
# provider later we only change this file.
#
# WHERE DOES THE EMAIL GO?
#   config/settings.py has EMAIL_BACKEND set to the "console" backend, which
#   PRINTS emails in the terminal instead of sending them. Perfect for
#   development: no account, no password, no spam by accident.
#   For the real thing, put the provider's SMTP settings in settings.py
#   (and keep the password OUT of Git).

from django.conf import settings
from django.core.mail import send_mail


class EmailService:
    """Sends one plain-text email."""

    def __init__(self, from_address=None):
        if from_address is None:
            from_address = settings.DEFAULT_FROM_EMAIL
        self.from_address = from_address      # UML: -fromAddress : String

    def send(self, to, subject, body):
        """
        UML: +send(to : String, subject : String, body : String) : Boolean
        Returns True when the email was handed over, False when it failed.
        """
        try:
            send_mail(subject, body, self.from_address, [to])
            return True
        except Exception:
            # Email can fail for reasons outside our control (the provider
            # is down, no internet...). We report False instead of crashing
            # so the job can carry on with the next student.
            return False
