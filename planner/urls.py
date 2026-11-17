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

# --- Step 2: Accounts (US-01, US-02) ---
from .controllers import account_controller

urlpatterns += [
    path("signup/", account_controller.sign_up, name="signup"),
    path("login/", account_controller.log_in, name="login"),
    path("logout/", account_controller.log_out, name="logout"),
]

# --- Step 3: Classes and activities (UC-09, UC-10) ---
from .controllers import course_controller

urlpatterns += [
    path("courses/", course_controller.show_courses, name="course_list"),
    path("courses/add/", course_controller.add_course, name="course_add"),
    path("courses/<int:course_id>/drop/", course_controller.drop_course, name="course_drop"),
]

# --- Step 4: The list and adding an item (US-05) ---
from .controllers import item_controller

urlpatterns += [
    path("items/", item_controller.show_list, name="item_list"),
    path("items/add/", item_controller.add_item, name="item_add"),
]

# --- Step 6: Edit, delete, complete, delete many, undo (US-04, US-07, US-08) ---
urlpatterns += [
    path("items/<int:item_id>/edit/", item_controller.edit_item, name="item_edit"),
    path("items/<int:item_id>/delete/", item_controller.delete_item, name="item_delete"),
    path("items/<int:item_id>/complete/", item_controller.mark_complete, name="item_complete"),
    path("items/delete-selected/", item_controller.delete_selected, name="items_delete_selected"),
    path("undo/", item_controller.undo, name="undo"),
]

# --- Step 8: Weekly calendar (US-13) ---
from .controllers import calendar_controller

urlpatterns += [
    path("calendar/", calendar_controller.show_week, name="calendar"),
    path("items/<int:item_id>/", calendar_controller.show_item, name="item_detail"),
]

# --- Step 9: Repeating events (US-06) ---
from .controllers import event_controller

urlpatterns += [
    path("events/add/", event_controller.add_event, name="event_add"),
    path("events/<int:event_id>/", event_controller.show_event, name="event_detail"),
    path("events/<int:event_id>/edit/", event_controller.edit_event, name="event_edit"),
    path("events/<int:event_id>/delete/", event_controller.delete_event, name="event_delete"),
]

# --- Step 10: Settings for the reminder email (US-11) ---
from .controllers import settings_controller

urlpatterns += [
    path("settings/", settings_controller.show_settings, name="settings"),
]
