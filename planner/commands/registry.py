# planner/commands/registry.py -- the list of command classes, by name.
#
# The invoker needs this for UNDO. Between two page loads it can only
# remember plain text: the NAME of the last command plus its memo. To undo,
# it looks the name up here to find the right class again.

_command_classes = {}


def register(command_class):
    """Adds one command class to the registry. Called in __init__.py."""
    _command_classes[command_class.name] = command_class


def get_command_class(name):
    """Returns the class for a command name, or None if it is unknown."""
    return _command_classes.get(name)
