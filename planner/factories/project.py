# planner/factories/project.py -- a CONCRETE CREATOR (Factory Method pattern).
# Read factories/base.py first: it explains the pattern.
#
# This ONE small file is everything Campus Hub knows about the "Project" type.

from datetime import time

from planner.models import Item, ItemType

from .base import ItemCreator


class ProjectCreator(ItemCreator):
    """Creates project deadlines (for example a team project milestone)."""

    type_code = ItemType.PROJECT
    label = "Project"
    icon = "bi-kanban"
    color = "info"

    def make_item(self):
        # Like assignments, projects default to an 11:59 PM deadline.
        return Item(item_type=self.type_code, due_time=time(23, 59))
