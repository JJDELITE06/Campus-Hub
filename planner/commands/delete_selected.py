# planner/commands/delete_selected.py -- "Delete several completed items at
# once" (UC-08, SD-08).
#
# This shows off a big advantage of the Command pattern: a command can be
# built OUT OF other commands (sometimes called a "macro command").
# We do not write any new delete logic here. We just create one
# DeleteItemCommand per selected item and run them one after another.
#
# data needs:  "item_ids"  = a list of item ids

from .base import Command
from .delete_item import DeleteItemCommand


class DeleteSelectedCommand(Command):
    name = "delete_selected"
    can_undo = True

    def execute(self):
        item_ids = self.data.get("item_ids", [])
        if len(item_ids) == 0:
            self.errors = ["Select at least one item first."]
            return False

        child_memos = []       # one memo per item that was really deleted
        for item_id in item_ids:
            child = DeleteItemCommand(self.student, {"item_id": item_id})
            if child.execute():
                child_memos.append(child.memo)

        self.deleted_count = len(child_memos)
        if self.deleted_count == 0:
            self.errors = ["Those items could not be found."]
            return False

        self.memo = {"children": child_memos}
        self.message = "Deleted " + str(self.deleted_count) + " item(s)."
        return True

    def undo(self):
        # Undo every small delete, one at a time.
        restored = 0
        for child_memo in self.memo.get("children", []):
            child = DeleteItemCommand(self.student, {})
            child.memo = child_memo
            if child.undo():
                restored = restored + 1
        self.message = "Brought back " + str(restored) + " item(s)."
        return restored > 0
