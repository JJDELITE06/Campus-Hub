# planner/factories/job_shift.py -- a CONCRETE CREATOR (Factory Method pattern).
# Read factories/base.py first: it explains the pattern.
#
# This ONE small file is everything Campus Hub knows about the "Job shift" type.

from planner.models import Item, ItemType

from .base import ItemCreator


class JobShiftCreator(ItemCreator):
    """Creates work shifts (work-study or an off-campus job)."""

    type_code = ItemType.JOB_SHIFT
    label = "Job shift"
    icon = "bi-briefcase"
    color = "warning"

    def make_item(self):
        return Item(item_type=self.type_code)

    def extra_errors(self, item):
        # Special rule: a shift has a start AND an end, so we know its length.
        errors = []
        if item.due_time is None or item.end_time is None:
            errors.append("A job shift needs a start time and an end time.")
        return errors
