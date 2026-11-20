# planner/models/item_type.py -- the ItemType enumeration (UML diagram CD-2).
#
# An ENUMERATION is a fixed list of allowed choices with names.
# Using names (ItemType.ASSIGNMENT) instead of typing the text "ASSIGNMENT"
# everywhere means a typo becomes an error right away instead of a hidden bug.
#
# NOTE: everything ELSE about a type (its label, icon, color and rules) lives
# in its "creator" class in the planner/factories folder. See factories/base.py.


class ItemType:
    """The kinds of planner item. These exact words are saved in the database."""

    ASSIGNMENT = "ASSIGNMENT"
    TEST_QUIZ = "TEST_QUIZ"
    PROJECT = "PROJECT"
    MEETING = "MEETING"
    CLASS = "CLASS"
    JOB_SHIFT = "JOB_SHIFT"
    CLUB_MEETING = "CLUB_MEETING"
    OTHER = "OTHER"
