# planner/commands/edit_item.py -- "Edit an item" (US-07, UC-05, SD-05).

from planner.factories import get_creator

from .base import Command


class EditItemCommand(Command):
    name = "edit_item"
    can_undo = True

    def execute(self):
        item = self.find_item(self.data.get("item_id"))
        if item is None:
            self.errors = ["That item could not be found."]
            return False

        # Take a "photo" of the item BEFORE changing it, so undo can put
        # everything back exactly as it was.
        before = item.to_form_data()

        # Apply the changes to the object in memory (not saved yet).
        item.update(self.data)

        # The student may have changed the TYPE, so we ask the creator of
        # the item's (possibly new) type for its special rules.
        creator = get_creator(item.item_type)
        if creator is None:
            self.errors = ["Please choose a type."]
            return False
        self.errors = item.validate() + creator.extra_errors(item)
        if self.errors:
            return False        # we never called save(), so nothing changed

        item.save()
        self.item = item
        self.memo = {"item_id": item.pk, "before": before}
        self.message = 'Saved your changes to "' + item.title + '".'
        return True

    def undo(self):
        item = self.find_item(self.memo.get("item_id"))
        if item is None:
            return False
        item.update(self.memo["before"])     # put the old values back
        item.save()
        self.message = 'Put "' + item.title + '" back the way it was.'
        return True
