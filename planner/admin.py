# planner/admin.py -- shows our models on Django's built-in admin site.
#
# Django gives every project a free "back office" at /admin/ where a
# superuser can look at and edit the database tables. It is great for
# checking what really got saved while we develop.
# Create a superuser with:   python manage.py createsuperuser

from django.contrib import admin

from .models import Course, Item, RepeatingEvent, Student

# One line per model switches it on in the admin site.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Item)
admin.site.register(RepeatingEvent)
