# planner/controllers/calendar_controller.py -- CalendarController (UML CD-5).
# The weekly calendar and the item details page (US-13, UC-13, SD-13).

from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from planner.form_tools import parse_date
from planner.models import Item
from planner.services.week_calendar import WeekCalendar

from .helpers import get_student


@login_required
def show_week(request):
    """UML: showWeek(weekStart : Date)   The address looks like /calendar/?week=2026-11-15"""
    student = get_student(request)

    # Which week? If the address has no (valid) date, use today's week.
    week_start = parse_date(request.GET.get("week", ""))
    calendar = WeekCalendar(student, week_start)

    # Build a simple list the template can loop over: one entry per day.
    days = []
    for day in calendar.get_days():
        days.append({
            "date": day,
            "is_today": day == date.today(),
            "items": calendar.get_items_for(day),
            "events": calendar.get_events_for(day),
        })

    context = {
        "days": days,
        "week_start": calendar.week_start,
        "week_end": calendar.week_start + timedelta(days=6),
        "is_empty": calendar.is_empty(),
        # The dates the Back and Forward buttons jump to.
        "previous_week": calendar.week_start - timedelta(days=7),
        "next_week": calendar.week_start + timedelta(days=7),
    }
    return render(request, "planner/calendar_week.html", context)


@login_required
def show_item(request, item_id):
    """UML: showItem(itemId)   Opens one item to see its details."""
    student = get_student(request)
    item = get_object_or_404(Item, pk=item_id, owner=student)
    return render(request, "planner/item_detail.html", {"item": item})
