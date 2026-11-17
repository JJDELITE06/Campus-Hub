# planner/factories/club_meeting.py -- a CONCRETE CREATOR (Factory Method pattern).
# Read factories/base.py first: it explains the pattern.
#
# This ONE small file is everything Campus Hub knows about the "Club meeting" type.

from planner.models import Item, ItemType

from .base import ItemCreator


class ClubMeetingCreator(ItemCreator):
    """Creates club and activity meetings (band, debate club...)."""

    type_code = ItemType.CLUB_MEETING
    label = "Club meeting"
    icon = "bi-music-note-beamed"
    color = "success"

    def make_item(self):
        return Item(item_type=self.type_code)

    def extra_errors(self, item):
        errors = []
        if item.due_time is None:
            errors.append("A club meeting needs a start time.")
        return errors
