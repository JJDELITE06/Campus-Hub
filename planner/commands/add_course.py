# planner/commands/add_course.py -- "Add a new class" (UC-09, SD-09).
#
# data needs:  "name", and optionally "code", "color", "is_activity"

from planner.models import Course

from .base import Command


class AddCourseCommand(Command):
    name = "add_course"

    def execute(self):
        course = Course(
            owner=self.student,
            name=self.data.get("name", "").strip(),
            code=self.data.get("code", "").strip(),
            color=self.data.get("color", "") or "#0d6efd",
            # A checkbox only sends a value when it is ticked.
            is_activity=bool(self.data.get("is_activity")),
        )
        self.errors = course.validate()
        if self.errors:
            return False

        course.save()
        self.course = course
        self.message = 'Added "' + course.get_name() + '".'
        return True
