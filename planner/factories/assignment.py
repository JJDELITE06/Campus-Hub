# planner/factories/assignment.py -- a CONCRETE CREATOR (Factory Method pattern).
# Read factories/base.py first: it explains the pattern.
#
# This ONE small file is everything Campus Hub knows about the "Assignment" type.

from datetime import time

from planner.models import Item, ItemType

from .base import ItemCreator


class AssignmentCreator(ItemCreator):      # "(ItemCreator)" = inherits from it
    """Creates homework-style items."""

    type_code = ItemType.ASSIGNMENT
    label = "Assignment"
    icon = "bi-pencil-square"
    color = "primary"

    def make_item(self):
        # THE FACTORY METHOD for assignments.
        # Special for this type: if the student leaves the time blank, an
        # assignment is due at 11:59 PM (the usual Blackboard deadline).
        return Item(item_type=self.type_code, due_time=time(23, 59))
