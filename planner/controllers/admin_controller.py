# planner/controllers/admin_controller.py -- AdminController (UML CD-5).
# The administrator (Jodi) can list, search and delete students
# (US-12, UC-16, SD-16).
#
# These pages are at /manage/... Django's own built-in admin site is a
# different thing and stays at /admin/.

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from planner.models import Administrator, Student

from .helpers import is_admin

# "@user_passes_test(is_admin)" means: only run the function when
# is_admin(user) is True. Everybody else is sent to the login page.


@user_passes_test(is_admin)
def show_students(request):
    """UML: showStudents(search : String)"""
    administrator = Administrator(request.user)
    search = request.GET.get("search", "")
    students = administrator.search_students(search)
    return render(request, "planner/admin_students.html", {"students": students, "search": search})


@user_passes_test(is_admin)
def delete_student(request, student_id):
    """UML: confirmDelete(studentId) on GET and deleteStudent(studentId) on POST"""
    student = get_object_or_404(Student, pk=student_id)

    if request.method != "POST":
        return render(request, "planner/admin_confirm_delete.html", {"student": student})

    if student.user == request.user:
        messages.error(request, "You can't delete your own account while logged in.")
    else:
        email = student.get_email()
        Administrator(request.user).delete_student(student)
        messages.success(request, "Deleted " + email + " and all of their data.")
    return redirect("manage_students")
