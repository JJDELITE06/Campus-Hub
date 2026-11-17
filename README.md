# Campus Hub

A student planning web app for assignments, tests, meetings, job shifts and more.
CS-312 Software Engineering, Team 5.

- Setup instructions: see docs/SETUP.md
- Problems and fixes: see docs/TIPS-TROUBLESHOOTING.md
- How the code is organized, the design patterns, and how to add to it: see docs/design/BUILD_PLAN.md

## Run it

```
python manage.py migrate        # create the database tables
python manage.py seed_demo      # optional sample data (sally@example.edu / campushub123)
python manage.py test           # run the unit tests
python manage.py runserver      # then open http://127.0.0.1:8000/
```
