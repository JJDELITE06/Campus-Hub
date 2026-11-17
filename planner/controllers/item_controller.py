# planner/controllers/item_controller.py -- ItemController (UML CD-5).
# The main list plus add, edit, delete, complete and undo.
#
# Look how short each function is: the controller only passes the request on
# to a COMMAND. All the rules are somewhere else.

from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from planner.commands import (
    AddItemCommand,
    DeleteItemCommand,
    DeleteSelectedCommand,
    EditItemCommand,
    MarkCompleteCommand,
)
from planner.factories import all_creators, get_creator
from planner.models import Item
from planner.services.item_filter import ItemFilter

from .helpers import get_invoker, get_student

# "@login_required" (used below) is a DECORATOR: a label you put on top of a
# function to add behaviour to it. This one means "if nobody is logged in,
# send them to the login page instead of running the function".


def form_page(request, student, data, errors, heading, item=None):
    """Shows the add/edit form. Shared by add_item() and edit_item()."""
    context = {
        "data": data,                      # what to put in the boxes
        "errors": errors,                  # problems to show at the top
        "heading": heading,                # "Add an item" or "Edit item"
        "item": item,                      # None when adding
        "creators": all_creators(),        # fills the Type dropdown (FACTORY)
        "courses": student.get_courses(),  # fills the Class dropdown
    }
    return render(request, "planner/item_form.html", context)


@login_required
def show_list(request):
    """UML: showList(filter : ItemFilter)   The main page (US-03, US-08, US-09)."""
    student = get_student(request)

    # ---- build the filter from the address, e.g. /items/?course=3&type=MEETING
    item_filter = ItemFilter()
    course_id = request.GET.get("course", "")
    type_code = request.GET.get("type", "")
    if course_id.isdigit():
        item_filter.set_course(student.courses.filter(pk=int(course_id)).first())
    if get_creator(type_code) is not None:
        item_filter.set_type(type_code)

    # ---- get this student's items and let the filter choose
    items = item_filter.apply(student.get_items())

    # ---- split into the two sections of the page
    today = date.today()
    to_do = []
    completed = []
    due_soon = []          # for the yellow reminder banner
    for item in items:
        if item.is_completed():
            completed.append(item)
        else:
            to_do.append(item)
            if today <= item.due_date <= today + timedelta(days=1):
                due_soon.append(item)

    context = {
        "to_do": to_do,
        "completed": completed,
        "due_soon": due_soon,
        "courses": student.get_courses(),
        "creators": all_creators(),
        "item_filter": item_filter,
        "selected_course": course_id,
        "selected_type": type_code,
    }
    return render(request, "planner/item_list.html", context)


@login_required
def add_item(request):
    """UML: showAddForm() and addItem(formData)   (US-05, SD-03)"""
    student = get_student(request)
    if request.method != "POST":
        # Start the date box on today, to save typing.
        data = {"due_date": date.today().strftime("%Y-%m-%d"), "item_type": "ASSIGNMENT"}
        return form_page(request, student, data, [], "Add an item")

    # request.POST.dict() turns the form into a normal Python dictionary.
    data = request.POST.dict()
    command = AddItemCommand(student, data)          # 1. build the command
    if get_invoker(request).run(command):            # 2. the invoker runs it
        messages.success(request, command.message, extra_tags="undo")
        return redirect("item_list")                 # 3. back to the list
    return form_page(request, student, data, command.errors, "Add an item")


@login_required
def edit_item(request, item_id):
    """UML: showEditForm(itemId) and editItem(itemId, formData)   (US-07, SD-05)"""
    student = get_student(request)
    # get_object_or_404: find the item, or show a "404 Not Found" page.
    # owner=student makes it impossible to open someone else's item (NFR-04).
    item = get_object_or_404(Item, pk=item_id, owner=student)

    if request.method != "POST":
        return form_page(request, student, item.to_form_data(), [], "Edit item", item)

    data = request.POST.dict()
    data["item_id"] = item_id
    command = EditItemCommand(student, data)
    if get_invoker(request).run(command):
        messages.success(request, command.message, extra_tags="undo")
        return redirect("item_list")
    return form_page(request, student, data, command.errors, "Edit item", item)


@login_required
def delete_item(request, item_id):
    """UML: deleteItem(itemId)   GET asks "are you sure?", POST deletes (US-04, SD-06)."""
    student = get_student(request)
    item = get_object_or_404(Item, pk=item_id, owner=student)

    if request.method != "POST":
        return render(request, "planner/item_confirm_delete.html", {"item": item})

    command = DeleteItemCommand(student, {"item_id": item_id})
    if get_invoker(request).run(command):
        messages.success(request, command.message, extra_tags="undo")
    return redirect("item_list")


@login_required
def delete_selected(request):
    """UML: deleteSelected(itemIds : List<int>)   (UC-08, SD-08)"""
    student = get_student(request)
    if request.method == "POST":
        # getlist() collects the value of EVERY ticked checkbox named "item_ids".
        item_ids = request.POST.getlist("item_ids")
        command = DeleteSelectedCommand(student, {"item_ids": item_ids})
        if get_invoker(request).run(command):
            messages.success(request, command.message, extra_tags="undo")
        else:
            messages.error(request, command.errors[0])
    return redirect("item_list")


@login_required
def mark_complete(request, item_id):
    """UML: markComplete(itemId, done : Boolean)   (US-08, SD-07)"""
    student = get_student(request)
    if request.method == "POST":
        # The button sends done=1 (mark complete) or done=0 (not done).
        done = request.POST.get("done") == "1"
        command = MarkCompleteCommand(student, {"item_id": item_id, "done": done})
        if get_invoker(request).run(command):
            messages.success(request, command.message, extra_tags="undo")
    return redirect("item_list")


@login_required
def undo(request):
    """The Undo button: asks the invoker to reverse the last command."""
    student = get_student(request)
    if request.method == "POST":
        command = get_invoker(request).undo_last(student)
        if command is None:
            messages.info(request, "There is nothing to undo.")
        else:
            messages.success(request, command.message)
    return redirect("item_list")
