# planner/commands/edit_repeating_event.py -- "Edit a repeating event",
# the "change ALL of them" choice in US-07.
#
# data needs: "event_id" plus the same form fields as AddRepeatingEventCommand

from .base import Command


class EditRepeatingEventCommand(Command):
    name = "edit_repeating_event"

    def execute(self):
        event = self.find_event(self.data.get("event_id"))
        if event is None:
            self.errors = ["That repeating event could not be found."]
            return False

        event.update_all(self.data)
        self.errors = event.validate()
        if self.errors:
            return False

        event.save()
        self.event = event
        self.message = 'Saved your changes to "' + event.title + '".'
        return True
