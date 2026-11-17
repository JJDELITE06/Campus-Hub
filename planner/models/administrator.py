# planner/models/administrator.py -- the Administrator class (UML CD-1).
#
# The persona "Jodi" is a system administrator. In Django, an administrator
# is simply a User whose "is_staff" switch is turned on.
#
# This class is a plain Python class (NOT a database table). It wraps a
# staff User and gives it the three methods from our UML diagram.
# It has no table of its own because it has no extra data to store.

from django.db.models import Q   # Q lets us say "this OR that" in a search

from .student import Student


class Administrator:
    """A staff user who can manage student accounts (US-12, UC-16)."""

    def __init__(self, user):
        # __init__ is the CONSTRUCTOR: it runs when we write Administrator(user).
        self.user = user

    def list_students(self):
        """UML: +listStudents() : List<Student>"""
        # select_related("user") is a speed-up: it fetches the Student and
        # its User in ONE database trip instead of two.
        return list(Student.objects.select_related("user").order_by("user__email"))

    def search_students(self, text):
        """UML: +searchStudents(text : String) : List<Student>"""
        text = text.strip()              # remove spaces at the start and end
        if text == "":
            return self.list_students()  # no search text = show everybody
        # icontains = "contains, ignoring upper/lower case"
        # The double underscore "user__email" means: follow the link to the
        # User, then look at its email.
        matches = Student.objects.select_related("user").filter(
            Q(user__email__icontains=text) | Q(user__first_name__icontains=text)
        )
        return list(matches.order_by("user__email"))

    def delete_student(self, student):
        """
        UML: +deleteStudent(student : Student) : void

        Deleting the User also deletes the Student, their courses, items and
        repeating events, because all of those links use on_delete=CASCADE.
        Afterwards the email is free, so the student can sign up again
        (US-12 acceptance criterion 6).
        """
        student.user.delete()
