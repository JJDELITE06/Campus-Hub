# planner/services/item_filter.py -- the ItemFilter class (UML diagram CD-3).
#
# Holds the student's filter choices and applies them to a list of items
# (US-03 filter by class/activity, US-09 filter by item type).
#
# It is a plain Python class: no database and no web code. That makes it
# very easy to unit test: give it a list, check the list that comes back.


class ItemFilter:
    """Remembers which items the student wants to see."""

    def __init__(self):
        # None means "no choice made", which shows everything ("All").
        self.course = None            # UML: -course : Course = null
        self.item_type = None         # UML: -type : ItemType = null
        self.show_completed = True    # UML: -showCompleted : Boolean = true

    def set_course(self, course):
        """UML: +setCourse(course : Course) : void"""
        self.course = course

    def set_type(self, item_type):
        """UML: +setType(type : ItemType) : void"""
        self.item_type = item_type

    def clear(self):
        """UML: +clear() : void   Back to showing everything."""
        self.course = None
        self.item_type = None
        self.show_completed = True

    def is_active(self):
        """True when at least one filter is switched on."""
        return self.course is not None or self.item_type is not None

    def apply(self, items):
        """
        UML: +apply(items : List<Item>) : List<Item>
        Returns a NEW list with only the items that pass every filter.
        The order of the items is kept.
        """
        result = []
        for item in items:
            # "continue" means: skip this item and go on to the next one.
            if self.course is not None and item.course_id != self.course.pk:
                continue
            if self.item_type is not None and item.item_type != self.item_type:
                continue
            if not self.show_completed and item.is_completed():
                continue
            result.append(item)
        return result
