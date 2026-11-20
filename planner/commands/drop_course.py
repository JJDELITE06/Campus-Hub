# planner/commands/drop_course.py -- "Drop a class" (UC-10, SD-10).
#
# data needs:  "course_id"

from .base import Command


class DropCourseCommand(Command):
    name = "drop_course"

    def execute(self):
        course = self.find_course(self.data.get("course_id"))
        if course is None:
            self.errors = ["That class could not be found."]
            return False

        name = course.get_name()
        # The Course object (the RECEIVER) does the real work.
        self.deleted_count = course.delete_with_items()
        self.message = (
            'Dropped "' + name + '" and deleted its '
            + str(self.deleted_count) + " item(s)."
        )
        return True
