# planner/controllers/ -- the CONTROLLER classes from UML diagram CD-5.
#
# A controller handles a request from a web page and sends a page back.
# (Django's own word for this is a "view". Same thing.)
#
# In the UML each controller is a class with methods. In Django the simplest
# way to write them is ONE FILE per controller with ONE FUNCTION per method:
#
#     UML                          our code
#     ItemController.addItem()     controllers/item_controller.py -> add_item()
#
# Every controller function follows the same three steps:
#     1. read what the browser sent (request)
#     2. build a COMMAND and give it to the INVOKER   (or just read some data)
#     3. send back a page (render) or jump to another page (redirect)
#
# The controllers contain NO business rules. Those live in the models,
# the factories and the commands. That is why the pages can change later
# without breaking the logic.
#
# HOW TO ADD A NEW PAGE:
#   1. Write a function in the right controller file (or a new file here).
#   2. Add one path(...) line to planner/urls.py.
#   3. Add a template in planner/templates/planner/.
