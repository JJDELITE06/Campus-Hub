# planner/controllers/course_controller.py -- CourseController (UML CD-5).
# List, add and drop classes and activities (UC-09, UC-10 / SD-09, SD-10).

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from planner.commands import AddCourseCommand, DropCourseCommand
from planner.models import Course

from .helpers import get_invoker, get_student


@login_required
def show_courses(request):
    """UML: showCourses()"""
    student = get_student(request)
    return render(request, "planner/course_list.html", {"courses": student.get_courses()})


@login_required
def add_course(request):
    """UML: showAddForm() and addCourse(name, code)"""
    student = get_student(request)
    if request.method != "POST":
        return render(request, "planner/course_form.html", {"data": {"color": "#0d6efd"}})

    data = request.POST.dict()
    command = AddCourseCommand(student, data)
    if get_invoker(request).run(command):
        messages.success(request, command.message)
        return redirect("course_list")
    return render(request, "planner/course_form.html", {"data": data, "errors": command.errors})


@login_required
def drop_course(request, course_id):
    """UML: confirmDrop(courseId) on GET and dropCourse(courseId) on POST"""
    student = get_student(request)
    course = get_object_or_404(Course, pk=course_id, owner=student)

    if request.method != "POST":
        # UC-10 step 3: ask "are you sure" and show how many items will go.
        return render(request, "planner/course_confirm_drop.html", {"course": course})

    command = DropCourseCommand(student, {"course_id": course_id})
    if get_invoker(request).run(command):
        messages.success(request, command.message)
    return redirect("course_list")
