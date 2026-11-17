# planner/commands/add_item.py -- "Add a single item" (US-05, UC-03, SD-03).
#
# This is where our TWO patterns meet:
#   the COMMAND (this class) asks the FACTORY for the right creator,
#   and the creator builds the item.
# Notice there is NO if/else on the item type anywhere in this file.

from planner.factories import get_creator

from .base import Command


class AddItemCommand(Command):
    name = "add_item"
    can_undo = True

    def execute(self):
        # 1. Find the creator for the type the student picked in the dropdown.
        creator = get_creator(self.data.get("item_type", ""))
        if creator is None:
            self.errors = ["Please choose a type."]
            return False

        # 2. Let the factory build the item (not saved yet).
        item = creator.create_item(self.student, self.data)

        # 3. Check it: the rules for ALL items + the rules for THIS type.
        self.errors = item.validate() + creator.extra_errors(item)
        if self.errors:          # a non-empty list counts as True in Python
            return False

        # 4. All good: save it and remember its id for undo.
        item.save()
        self.item = item
        self.memo = {"item_id": item.pk}     # pk = "primary key" = the row's id
        self.message = 'Added "' + item.title + '".'
        return True

    def undo(self):
        # Undoing an "add" means deleting the item we added.
        item = self.find_item(self.memo.get("item_id"))
        if item is None:
            return False
        self.message = 'Removed "' + item.title + '" again.'
        item.delete()
        return True
