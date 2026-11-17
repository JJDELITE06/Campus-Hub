# planner/urls.py -- WHICH web address runs WHICH controller function.
#
# Each path(...) line has three parts:
#     path("address/", the_function_to_run, name="nickname")
# The nickname lets templates write {% url 'item_add' %} instead of the
# address, so we can change an address here without hunting through pages.
#
# "<int:item_id>" is a blank in the address: /items/7/edit/ runs
# edit_item(request, item_id=7).
#
# HOW THIS FILE GROWS: every build step adds ONE block at the bottom:
# an import of its controller, and its addresses added to the list with +=
# ("+=" means "add these to the end of the list"). Nobody edits another
# step's block, so two people rarely change the same lines.

from django.urls import path

urlpatterns = []       # start with an empty list of addresses

# --- Step 1: The home page ---
from .controllers import home_controller

urlpatterns += [
    path("", home_controller.home, name="home"),
]
