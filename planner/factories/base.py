# planner/factories/base.py -- the FACTORY METHOD pattern: the parent "Creator".
#
# ============================ THE PROBLEM ====================================
# The planner has many kinds of item (assignment, quiz, meeting, job shift...)
# and we will add more. WITHOUT a pattern, the "add item" code turns into one
# giant block like this:
#
#       if item_type == "ASSIGNMENT":   ... set the default time to 11:59 PM ...
#       elif item_type == "MEETING":    ... make sure there is a location ...
#       elif item_type == "JOB_SHIFT":  ... make sure there is an end time ...
#       elif ...                        (grows forever)
#
# Every new type means EDITING that block, and one typo breaks every type.
#
# ============================ THE PATTERN ====================================
# Factory Method (a "creational" pattern from the Gang of Four book):
#
#   * The CREATOR (this class, ItemCreator) holds the steps that are THE SAME
#     for every type, in create_item().
#   * One step, make_item(), is left EMPTY on purpose. It is the
#     "FACTORY METHOD".
#   * Each CONCRETE CREATOR (AssignmentCreator, MeetingCreator...) is a small
#     subclass in its own file that fills in make_item() for its own type.
#
# RESULT: adding a new type = adding ONE new file. Nobody edits working code.
# (This is the "Open/Closed Principle": open for extension, closed for change.)
#
# TRADEOFFS: more classes and more files than one if/else block, and when
# debugging you step through two classes instead of one.
#
# NOTE FOR OUR DESIGN DOC: in the textbook version each creator returns a
# different product SUBCLASS. Our UML (CD-2) has a single Item class with a
# "type" attribute, so every creator returns an Item that is set up for its
# type. Same pattern, simpler database (one table).

from abc import ABC, abstractmethod   # ABC = "Abstract Base Class"


class ItemCreator(ABC):
    """
    The abstract Creator. "Abstract" means you can NOT make an object from
    this class directly. It only exists to be the parent of real creators.
    """

    # ---- Each concrete creator REPLACES these four class attributes ----
    type_code = ""         # the word saved in the database, e.g. "ASSIGNMENT"
    label = ""             # what the student sees, e.g. "Assignment"
    icon = "bi-circle"     # a Bootstrap Icons name (https://icons.getbootstrap.com)
    color = "secondary"    # a Bootstrap color name: primary, success, danger...

    def create_item(self, owner, data):
        """
        The steps EVERY type shares. Subclasses do NOT override this method.

        owner = the Student who is adding the item
        data  = the dictionary of text from the web form

        Returns a new Item that is NOT saved yet (the caller checks it first).
        """
        # Step 1: ask the subclass for a brand-new item of ITS type.
        #         This line is the heart of the pattern: this parent class
        #         does not know (or care) which concrete creator it is.
        item = self.make_item()

        # Step 2: every item belongs to the student who created it.
        item.owner = owner

        # Step 3: copy in what the student typed. We skip boxes that were
        #         left BLANK, so the defaults from step 1 stay in place
        #         (for example an assignment's 11:59 PM due time).
        filled_in = {}
        for key, value in data.items():
            if value != "":
                filled_in[key] = value
        item.update(filled_in)

        # Step 4: stamp the type LAST so the form can never change it.
        item.item_type = self.type_code
        return item

    @abstractmethod
    def make_item(self):
        """
        THE FACTORY METHOD. Every concrete creator MUST write its own version
        and return a new, empty Item set up for its type.

        @abstractmethod makes Python refuse to create a subclass object that
        forgot to write this method. The mistake shows up immediately.
        """

    def extra_errors(self, item):
        """
        Rules that only apply to ONE type. The default is "no extra rules".
        A concrete creator overrides this when its type has special rules
        (for example: a job shift must have an end time).
        Returns a list of error messages, like Item.validate().
        """
        return []
