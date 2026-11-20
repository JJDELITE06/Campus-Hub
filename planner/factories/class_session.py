# planner/factories/class_session.py -- a CONCRETE CREATOR (Factory Method pattern).
# Read factories/base.py first: it explains the pattern.
#
# This ONE small file is everything Campus Hub knows about the "Class" type.

from planner.models import Item, ItemType

from .base import ItemCreator


class ClassSessionCreator(ItemCreator):
    """Creates a class session (a lecture or a lab)."""

    type_code = ItemType.CLASS
    label = "Class"
    icon = "bi-mortarboard"
    color = "dark"

    def make_item(self):
        return Item(item_type=self.type_code)

    def extra_errors(self, item):
        errors = []
        if item.due_time is None:
            errors.append("A class needs a start time.")
        return errors
