# planner/commands/base.py -- the COMMAND pattern: the parent "Command" class.
#
# ============================ THE PROBLEM ====================================
# WITHOUT a pattern, the code that handles a button click (the controller)
# would also contain all the logic for adding, editing, deleting... The screen
# code and the "what actually happens" code get tangled together. That is
# BRITTLE: changing a page can break the logic, and the logic can't be reused
# (for example by an "undo" button or an import feature).
#
# ============================ THE PATTERN ====================================
# Command (a "behavioral" pattern from the Gang of Four book):
#   Turn each REQUEST ("add this item", "delete that item") into an OBJECT
#   that holds everything needed to carry it out.
#
#   The four roles, and where they are in Campus Hub:
#     COMMAND   this class: the common interface. Every command has execute().
#     CONCRETE  one small class per action, one file each (add_item.py...).
#     INVOKER   commands/invoker.py. It runs commands without knowing what
#               they do, and remembers the last one so it can be undone.
#     RECEIVER  the model objects (Item, Course...) that do the real work.
#     CLIENT    the controllers: they build a command and hand it over.
#
#   Think of a TV remote: every button just says "execute". The remote does
#   not know how a TV changes channel.
#
# RESULT: a new action = ONE new file. Undo and "delete many at once" become
# easy because a command is an object we can store and reuse.
#
# TRADEOFF: more small classes than writing the logic straight in the view.

from abc import ABC, abstractmethod


class Command(ABC):
    """The abstract Command. Every action in Campus Hub is a subclass."""

    # ---- each concrete command replaces these two class attributes ----
    name = ""           # a short unique name, e.g. "add_item"
    can_undo = False    # True when the command has a working undo()

    def __init__(self, student, data):
        """
        EVERY command is built the same way:
            student = the logged-in Student (commands only ever touch
                      THIS student's data. That is requirement NFR-04).
            data    = a dictionary with everything the request needs,
                      usually the text from a web form plus an id.
        """
        self.student = student
        self.data = data

        # Filled in by execute():
        self.errors = []    # problems to show the student (empty = success)
        self.message = ""   # a friendly success sentence for the page
        self.memo = {}      # notes the command keeps so undo() can work.
                            # Only plain text/numbers, so it can be stored
                            # between two page loads.

    @abstractmethod
    def execute(self):
        """
        Do the action. Returns True if it worked, False if it did not
        (and then self.errors says why).
        """

    def undo(self):
        """
        Reverse the action, using self.memo. Returns True if it worked.
        Commands that can't be undone just keep this default.
        """
        return False

    # ---------- small helpers shared by many commands ----------
    # Each one looks ONLY inside this student's own data. Asking for another
    # student's id simply finds nothing (None).

    def find_item(self, item_id):
        return self.student.items.filter(pk=item_id).first()

    def find_course(self, course_id):
        return self.student.courses.filter(pk=course_id).first()

    def find_event(self, event_id):
        return self.student.events.filter(pk=event_id).first()
