# planner/commands/__init__.py -- switches the commands ON.
#
# HOW TO ADD A NEW COMMAND (for example "duplicate an item"):
#   1. Copy commands/mark_complete.py to a new file, e.g. duplicate_item.py
#   2. Give the class a new name and a new   name = "duplicate_item"
#   3. Write execute() (and undo() if you set can_undo = True).
#   4. Add TWO lines at the bottom of this file:
#          from .duplicate_item import DuplicateItemCommand
#          register(DuplicateItemCommand)
#   5. Add a test file in planner/tests/ and run the tests.
# Then a controller can run it with:   invoker.run(DuplicateItemCommand(student, data))

from .base import Command
from .invoker import CommandInvoker
from .registry import get_command_class, register

# --- Step 3: Classes and activities ---
from .add_course import AddCourseCommand
register(AddCourseCommand)

from .drop_course import DropCourseCommand
register(DropCourseCommand)

# --- Step 4: Add an item ---
from .add_item import AddItemCommand
register(AddItemCommand)

# --- Step 6: Edit, delete, complete, delete many ---
from .edit_item import EditItemCommand
register(EditItemCommand)

from .delete_item import DeleteItemCommand
register(DeleteItemCommand)

from .mark_complete import MarkCompleteCommand
register(MarkCompleteCommand)

from .delete_selected import DeleteSelectedCommand
register(DeleteSelectedCommand)

# --- Step 9: Repeating events ---
from .add_repeating_event import AddRepeatingEventCommand
register(AddRepeatingEventCommand)

from .edit_repeating_event import EditRepeatingEventCommand
register(EditRepeatingEventCommand)

from .delete_repeating_event import DeleteRepeatingEventCommand
register(DeleteRepeatingEventCommand)
