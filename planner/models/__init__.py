# planner/models/__init__.py -- the "table of contents" for our MODEL classes.
#
# WHAT IS A MODEL?
#   A model is a Python class that Django saves in the database for us.
#   One class = one database table. One object = one row in that table.
#   We never write SQL: Django's "ORM" (Object-Relational Mapper) does it.
#
# WHY IS THIS A FOLDER AND NOT ONE BIG models.py FILE?
#   Each class lives in its OWN file. That way two teammates can work on
#   two different classes at the same time and Git will not complain about
#   conflicts, because they are editing different files.
#
# HOW TO ADD A NEW MODEL CLASS (the only "hook" you need):
#   1. Create a new file in this folder, for example  grade.py
#   2. Add ONE import line at the bottom of this file:
#          from .grade import Grade
#   3. Run:  python manage.py makemigrations   then   python manage.py migrate
#
# Django only looks in "planner.models" for models, so a class that is not
# imported here is invisible to Django. That is why the import lines matter.

# All the model classes arrive together in Step 1, because they depend on
# each other (an Item points at a Course, a Course points at a Student...).

# The people
from .student import Student
from .administrator import Administrator

# Classes and activities
from .course import Course

# Planner items
from .item_type import ItemType
from .item import Item

# Repeating events
from .repeating_event import RepeatingEvent
