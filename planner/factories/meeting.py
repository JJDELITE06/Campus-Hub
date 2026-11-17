# planner/factories/meeting.py -- a CONCRETE CREATOR (Factory Method pattern).
# Read factories/base.py first: it explains the pattern.
#
# This ONE small file is everything Campus Hub knows about the "Meeting" type.

from planner.models import Item, ItemType

from .base import ItemCreator


class MeetingCreator(ItemCreator):
    """Creates one-time meetings (team meeting, office hours, advisor...)."""

    type_code = ItemType.MEETING
    label = "Meeting"
    icon = "bi-people"
    color = "success"

    def make_item(self):
        return Item(item_type=self.type_code)

    def extra_errors(self, item):
        # Special rules: a meeting needs a time and a place (or a Teams link).
        errors = []
        if item.due_time is None:
            errors.append("A meeting needs a start time.")
        if item.location == "":
            errors.append("A meeting needs a location (a room, Teams, etc.).")
        return errors
