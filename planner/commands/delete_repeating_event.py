# planner/commands/delete_repeating_event.py -- delete a repeating event,
# either EVERY date or JUST ONE date ("change one or all", US-07 / UC-06).
#
# data needs: "event_id", and optionally "only_date" (text "2026-11-26").
#             With "only_date" just that one day is removed.

from planner.form_tools import parse_date

from .base import Command


class DeleteRepeatingEventCommand(Command):
    name = "delete_repeating_event"

    def execute(self):
        event = self.find_event(self.data.get("event_id"))
        if event is None:
            self.errors = ["That repeating event could not be found."]
            return False

        only_date = parse_date(self.data.get("only_date", ""))
        if only_date is not None:
            event.delete_one(only_date)        # just this one date
            self.message = (
                'Removed "' + event.title + '" on '
                + only_date.strftime("%a %b %d") + " only."
            )
        else:
            self.message = 'Deleted every date of "' + event.title + '".'
            event.delete_all()                 # the whole series
        return True
