# planner/commands/delete_item.py -- "Delete an item" (US-04, UC-06, SD-06).

from planner.factories import get_creator_or_default

from .base import Command


class DeleteItemCommand(Command):
    name = "delete_item"
    can_undo = True

    def execute(self):
        item = self.find_item(self.data.get("item_id"))
        if item is None:
            self.errors = ["That item could not be found."]
            return False

        # Remember everything about the item so undo can bring it back.
        self.memo = {"before": item.to_form_data(), "completed": item.completed}
        self.message = 'Deleted "' + item.title + '".'
        item.delete()
        return True

    def undo(self):
        # Undoing a delete means building the item again from the memo.
        # We reuse the FACTORY, so the item is rebuilt the same way it was
        # first created. (It gets a new id, which nobody notices.)
        before = self.memo.get("before")
        if before is None:
            return False
        creator = get_creator_or_default(before["item_type"])
        item = creator.create_item(self.student, before)
        item.completed = self.memo.get("completed", False)
        item.save()
        self.message = 'Brought back "' + item.title + '".'
        return True
