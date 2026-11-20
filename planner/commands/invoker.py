# planner/commands/invoker.py -- the INVOKER of the Command pattern.
#
# The invoker's whole job is to RUN commands. It does not know or care
# whether a command adds, deletes or emails. It only calls execute().
#
# It also remembers the last undoable command, which is how the "Undo"
# button on the web page works.
#
# WHY "memory" IS PASSED IN:
#   A web server forgets everything between two page loads. Django gives each
#   logged-in browser a small notebook called the SESSION that survives
#   between pages. The controller passes that notebook in as "memory".
#   In unit tests we pass a plain dictionary {} instead, so the invoker can
#   be tested without a browser.

from .registry import get_command_class

# The page of the notebook where we write the last command.
MEMORY_KEY = "last_command"


class CommandInvoker:
    """Runs commands and remembers the last one that can be undone."""

    def __init__(self, memory):
        self.memory = memory     # request.session, or a plain dict in tests

    def run(self, command):
        """Executes a command. Returns True if it worked."""
        worked = command.execute()

        if worked and command.can_undo:
            # Remember just enough to rebuild the command later.
            self.memory[MEMORY_KEY] = {"name": command.name, "memo": command.memo}
        elif worked:
            # A command that can't be undone wipes the memory, so the Undo
            # button can never undo something older by surprise.
            self.memory.pop(MEMORY_KEY, None)
        return worked

    def undo_last(self, student):
        """
        Undoes the most recent undoable command.
        Returns the command object (so the page can show its message),
        or None when there was nothing to undo.
        """
        # pop = "take it out of the notebook", so one action is undone once.
        saved = self.memory.pop(MEMORY_KEY, None)
        if saved is None:
            return None

        command_class = get_command_class(saved["name"])
        if command_class is None:
            return None

        # Rebuild an empty command of the right class, give it back its
        # memo, and let IT decide how to reverse itself.
        command = command_class(student, {})
        command.memo = saved["memo"]
        if command.undo():
            return command
        return None
