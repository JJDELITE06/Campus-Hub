# planner/factories/registry.py -- the list of creators Campus Hub knows about.
#
# A REGISTRY is just a dictionary that maps a type code to its creator:
#       {"ASSIGNMENT": <AssignmentCreator object>, "MEETING": <MeetingCreator>...}
#
# The rest of the program asks the registry "give me the creator for MEETING"
# and never needs an if/else chain. Looking something up in a dictionary
# REPLACES the if/else.

# The underscore at the start of the name is a Python habit that means
# "private: code outside this file should use the functions below instead".
_creators = {}


def register(creator_class):
    """Adds one creator to the registry. Called once per type in __init__.py."""
    creator = creator_class()                  # make ONE object from the class
    _creators[creator.type_code] = creator     # file it under its type code


def get_creator(type_code):
    """Returns the creator for a type code, or None if we don't know the type."""
    return _creators.get(type_code)


def get_creator_or_default(type_code):
    """
    Like get_creator(), but falls back to the "Other" creator.
    The web pages use this to show a label and icon. If the database holds a
    type that this copy of the code does not know yet (for example a teammate
    added a type on a branch that is not merged), the page still works.
    """
    creator = _creators.get(type_code)
    if creator is None:
        creator = _creators.get("OTHER")
    return creator


def all_creators():
    """Returns every creator, in the order they were registered (for dropdowns)."""
    return list(_creators.values())
