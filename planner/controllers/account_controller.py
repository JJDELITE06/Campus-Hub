# planner/controllers/account_controller.py -- AccountController (UML CD-5).
# Sign up, log in, log out (US-01, US-02 / UC-01, UC-02 / SD-01, SD-02).

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from planner.models import Student


def sign_up(request):
    """UML: showSignUpForm() and signUp(name, email, password)"""
    # A browser asks for a page with GET and sends a filled-in form with POST.
    # So: GET = "show me the empty form", POST = "here is my form, save it".
    if request.method != "POST":
        return render(request, "planner/signup.html", {"data": {}})

    # .get(key, "") reads one box of the form ("" if it is missing).
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip().lower()   # emails ignore case
    password = request.POST.get("password", "")
    password_again = request.POST.get("password_again", "")

    # Check every box and collect ALL the problems, so the student can fix
    # them in one go.
    errors = []
    if name == "":
        errors.append("Please enter your name.")
    if "@" not in email:
        errors.append("Please enter a valid email address.")
    elif User.objects.filter(username=email).exists():
        errors.append("An account with this email already exists. Try logging in.")
    if len(password) < 8:
        errors.append("Your password needs at least 8 characters.")
    elif password != password_again:
        errors.append("The two passwords do not match.")

    if errors:
        # Show the form again and keep what they typed (but never the password).
        data = {"name": name, "email": email}
        return render(request, "planner/signup.html", {"data": data, "errors": errors})

    # create_user() HASHES the password (NFR-03): the real password is never
    # stored. We use the email as the login name.
    user = User.objects.create_user(
        username=email, email=email, password=password, first_name=name
    )
    Student.objects.create(user=user)    # reminders are ON by default (US-11)

    login(request, user)                 # log them straight in
    messages.success(request, "Welcome to Campus Hub, " + name + "!")
    return redirect("home")       # home() sends a logged-in student to their planner


def log_in(request):
    """UML: showLoginForm() and logIn(email, password)"""
    if request.method != "POST":
        return render(request, "planner/login.html", {"data": {}})

    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "")

    # authenticate() checks the password against the stored hash.
    # It returns the User, or None if the email or password is wrong.
    user = authenticate(request, username=email, password=password)
    if user is None:
        # We do NOT say which one was wrong. That would help someone guess.
        errors = ["Email or password is incorrect."]
        return render(request, "planner/login.html", {"data": {"email": email}, "errors": errors})

    login(request, user)
    return redirect("home")       # home() sends a logged-in student to their planner


def log_out(request):
    """UML: logOut()   Clears the session and goes back to the login page."""
    if request.method == "POST":
        logout(request)
    return redirect("login")
