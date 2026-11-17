# planner/commands/mark_complete.py -- "Mark an item complete" (US-08, UC-07).
#
# data needs:  "item_id"  and  "done"  (True = complete, False = not done)

from .base import Command


class MarkCompleteCommand(Command):
    name = "mark_complete"
    can_undo = True

    def execute(self):
        item = self.find_item(self.data.get("item_id"))
        if item is None:
            self.errors = ["That item could not be found."]
            return False

        self.memo = {"item_id": item.pk, "was_completed": item.completed}

        if self.data.get("done"):
            item.mark_complete()
            self.message = 'Nice work! "' + item.title + '" is done.'
        else:
            item.mark_not_done()
            self.message = '"' + item.title + '" is back on your to-do list.'
        return True

    def undo(self):
        item = self.find_item(self.memo.get("item_id"))
        if item is None:
            return False
        if self.memo.get("was_completed"):
            item.mark_complete()
        else:
            item.mark_not_done()
        self.message = 'Undid the change to "' + item.title + '".'
        return True
