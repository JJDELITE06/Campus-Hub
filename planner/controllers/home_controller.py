# planner/controllers/home_controller.py -- the front door of Campus Hub.
#
# The address "/" (nothing after the site name) runs home() below.

from django.shortcuts import redirect, render


def home(request):
    """Visitors see the welcome page. Logged-in students go to their planner."""
    if request.user.is_authenticated:
        # redirect("item_list") means "jump to the address nicknamed item_list".
        return redirect("item_list")
    # render() fills in an HTML template and sends it back as a web page.
    return render(request, "planner/welcome.html")
