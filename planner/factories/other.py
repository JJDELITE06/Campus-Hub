# planner/factories/other.py -- a CONCRETE CREATOR (Factory Method pattern).
# Read factories/base.py first: it explains the pattern.
#
# This ONE small file is everything Campus Hub knows about the "Other" type.

from planner.models import Item, ItemType

from .base import ItemCreator


class OtherCreator(ItemCreator):
    """Creates anything that does not fit another type. No special rules."""

    type_code = ItemType.OTHER
    label = "Other"
    icon = "bi-three-dots"
    color = "secondary"

    def make_item(self):
        return Item(item_type=self.type_code)
