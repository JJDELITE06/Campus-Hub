# planner/factories/test_quiz.py -- a CONCRETE CREATOR (Factory Method pattern).
# Read factories/base.py first: it explains the pattern.
#
# This ONE small file is everything Campus Hub knows about the "Test / Quiz" type.

from planner.models import Item, ItemType

from .base import ItemCreator


class TestQuizCreator(ItemCreator):
    """Creates tests, quizzes and exams."""

    type_code = ItemType.TEST_QUIZ
    label = "Test / Quiz"
    icon = "bi-patch-question"
    color = "danger"

    def make_item(self):
        return Item(item_type=self.type_code)

    def extra_errors(self, item):
        # Special rule for this type: you need to know WHEN to show up.
        errors = []
        if item.due_time is None:
            errors.append("A test or quiz needs a start time.")
        return errors
