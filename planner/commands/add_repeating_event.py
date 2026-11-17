# planner/commands/add_repeating_event.py -- "Add a repeating event"
# (US-06, UC-04, SD-04).
#
# data needs: "title", "item_type", "days_of_week" (text like "MON,THU"),
#             "start_time", "end_time", "first_date", "last_date",
#             and optionally "location" and "course_id"

from planner.factories import get_creator
from planner.models import RepeatingEvent

from .base import Command


class AddRepeatingEventCommand(Command):
    name = "add_repeating_event"

    def execute(self):
        event = RepeatingEvent(owner=self.student)
        event.update_all(self.data)

        self.errors = event.validate()
        if get_creator(event.item_type) is None:
            self.errors.append("Please choose a type.")
        if self.errors:
            return False

        event.save()
        self.event = event
        self.message = 'Added the repeating event "' + event.title + '".'
        return True
