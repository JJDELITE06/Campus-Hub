# planner/tests/helpers.py -- shortcuts used by many test files.

from django.contrib.auth.models import User

from planner.models import Student


def make_student(email="sally@example.edu", name="Sally", password="password123"):
    """Creates a User plus its Student and returns the Student."""
    user = User.objects.create_user(
        username=email, email=email, password=password, first_name=name
    )
    return Student.objects.create(user=user)


class FakeEmailService:
    """
    A stand-in for EmailService that sends nothing. It just remembers what
    it was asked to send, so a test can look at it afterwards.
    (This kind of stand-in is called a "test double" or a "fake".)
    """

    def __init__(self, works=True):
        self.works = works     # set to False to pretend sending fails
        self.sent = []         # a list of (to, subject, body)

    def send(self, to, subject, body):
        if self.works:
            self.sent.append((to, subject, body))
        return self.works
