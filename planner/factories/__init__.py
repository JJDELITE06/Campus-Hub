# planner/factories/__init__.py -- switches the item types ON.
#
# HOW TO ADD A NEW ITEM TYPE (for example "Internship deadline" for Carl):
#   1. Copy factories/other.py to a new file, e.g. factories/internship.py
#   2. Change the class name, type_code, label, icon and color in the copy.
#      (Optional: add the new word to models/item_type.py so there is a name
#      for it.)
#   3. Add TWO lines at the bottom of this file:
#          from .internship import InternshipCreator
#          register(InternshipCreator)
#   4. Add a test to tests/test_step05_item_types.py and run the tests.
#
# That's it. No database migration, no changes to the forms, the list, the
# calendar or the filters. They all read their types from this registry.

from .base import ItemCreator
from .registry import all_creators, get_creator, get_creator_or_default, register

# --- Step 4: the first type ---
from .assignment import AssignmentCreator
register(AssignmentCreator)

# --- Step 5: one small file per type (a good task to share out) ---
from .test_quiz import TestQuizCreator
register(TestQuizCreator)

from .project import ProjectCreator
register(ProjectCreator)

from .meeting import MeetingCreator
register(MeetingCreator)

from .class_session import ClassSessionCreator
register(ClassSessionCreator)

from .job_shift import JobShiftCreator
register(JobShiftCreator)

from .club_meeting import ClubMeetingCreator
register(ClubMeetingCreator)

from .other import OtherCreator
register(OtherCreator)
