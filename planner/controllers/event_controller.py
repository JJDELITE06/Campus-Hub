# planner/controllers/event_controller.py -- repeating events (US-06, UC-04).
#
# UML NOTE: in diagram CD-5 these methods sit inside ItemController
# (addRepeatingEvent...). We gave them their own file so the person building
# repeating events never edits the same file as the person building items.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from planner.commands import (
    AddRepeatingEventCommand,
    DeleteRepeatingEventCommand,
    EditRepeatingEventCommand,
)
from planner.factories import all_creators
from planner.form_tools import parse_date
from planner.models import RepeatingEvent

from .helpers import get_invoker, get_student

# The checkboxes on the form: (code saved in the database, label on screen).
DAY_CHOICES = [
    ("SUN", "Sun"), ("MON", "Mon"), ("TUE", "Tue"), ("WED", "Wed"),
    ("THU", "Thu"), ("FRI", "Fri"), ("SAT", "Sat"),
]


def read_event_form(request):
    """Turns the submitted form into the dictionary the commands expect."""
    data = request.POST.dict()
    # The day checkboxes arrive as a list, e.g. ["MON", "THU"].
    # The model stores them as the text "MON,THU".
    data["days_of_week"] = ",".join(request.POST.getlist("days"))
    return data


def event_form_page(request, student, data, errors, heading, event=None):
    """Shows the add/edit form for a repeating event."""
    context = {
        "data": data,
        "errors": errors,
        "heading": heading,
        "event": event,
        "creators": all_creators(),
        "courses": student.get_courses(),
        "day_choices": DAY_CHOICES,
        "chosen_days": data.get("days_of_week", "").split(","),
    }
    return render(request, "planner/event_form.html", context)


@login_required
def add_event(request):
    """UML: addRepeatingEvent(formData)"""
    student = get_student(request)
    if request.method != "POST":
        return event_form_page(request, student, {"item_type": "CLASS"}, [], "Add a repeating event")

    data = read_event_form(request)
    command = AddRepeatingEventCommand(student, data)
    if get_invoker(request).run(command):
        messages.success(request, command.message)
        return redirect("calendar")
    return event_form_page(request, student, data, command.errors, "Add a repeating event")


@login_required
def show_event(request, event_id):
    """Details of one repeating event, with the "just this one / all" buttons."""
    student = get_student(request)
    event = get_object_or_404(RepeatingEvent, pk=event_id, owner=student)
    # When opened from the calendar, the address says which date was clicked.
    clicked_date = parse_date(request.GET.get("date", ""))
    return render(request, "planner/event_detail.html", {"event": event, "clicked_date": clicked_date})


@login_required
def edit_event(request, event_id):
    """Change EVERY date of a repeating event (US-07)."""
    student = get_student(request)
    event = get_object_or_404(RepeatingEvent, pk=event_id, owner=student)
    if request.method != "POST":
        return event_form_page(request, student, event.to_form_data(), [], "Edit repeating event", event)

    data = read_event_form(request)
    data["event_id"] = event_id
    command = EditRepeatingEventCommand(student, data)
    if get_invoker(request).run(command):
        messages.success(request, command.message)
        return redirect("calendar")
    return event_form_page(request, student, data, command.errors, "Edit repeating event", event)


@login_required
def delete_event(request, event_id):
    """Delete ONE date (the form sends only_date) or ALL dates of an event."""
    student = get_student(request)
    if request.method == "POST":
        data = {"event_id": event_id, "only_date": request.POST.get("only_date", "")}
        command = DeleteRepeatingEventCommand(student, data)
        if get_invoker(request).run(command):
            messages.success(request, command.message)
        else:
            messages.error(request, command.errors[0])
    return redirect("calendar")
