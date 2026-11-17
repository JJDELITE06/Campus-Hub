# planner/controllers/settings_controller.py -- SettingsController (UML CD-5).
# Turn the daily reminder email on or off (US-11, UC-15, SD-15).

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .helpers import get_student


@login_required
def show_settings(request):
    """UML: showSettings() on GET and saveReminderSetting(on) on POST"""
    student = get_student(request)

    if request.method == "POST":
        # A switch (checkbox) is only sent by the browser when it is ON.
        turned_on = request.POST.get("reminders_on") == "on"
        # This change is one line, so we call the model directly instead of
        # writing a Command class for it. Not everything needs a pattern!
        student.set_reminders(turned_on)
        if turned_on:
            messages.success(request, "Daily reminder emails are ON.")
        else:
            messages.success(request, "Daily reminder emails are OFF.")
        return redirect("settings")

    return render(request, "planner/settings.html", {"student": student})
