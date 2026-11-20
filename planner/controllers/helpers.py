# planner/controllers/helpers.py -- small helpers shared by the controllers.

from planner.commands import CommandInvoker
from planner.models import Student


def get_student(request):
    """
    Returns the Student object for the person who is logged in.

    get_or_create means: "find it, and if it does not exist yet, create it".
    That covers users made outside our sign-up page, for example with
    "python manage.py createsuperuser".
    """
    student, was_created = Student.objects.get_or_create(user=request.user)
    return student


def get_invoker(request):
    """
    Returns the Command pattern INVOKER for this browser.
    request.session is the small "notebook" Django keeps for each logged-in
    browser. The invoker writes the last command in it so Undo can work.
    """
    return CommandInvoker(request.session)


def is_admin(user):
    """True when the logged-in user is an administrator (staff)."""
    return user.is_authenticated and user.is_staff
