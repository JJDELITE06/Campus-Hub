# Campus Hub: Build Plan, Module Guide and Unit Test Plan

This document explains how the Campus Hub code is organized, which class does what,
how the two design patterns are used, and how to add to the project without breaking it.
It also covers deliverable 4 of the final project ("detailed design document showing
modules and unit test plans").

---

## 1. Run it (5 commands)

Open the `Campus-Hub` folder in VS Code, open a terminal (the prompt must show `(.venv)`), then:

```
pip install -r requirements.txt      # only if Django is not installed yet
python manage.py migrate             # creates the database tables (first time, and after pulling new migrations)
python manage.py seed_demo           # optional: adds sample data
python manage.py test                # runs all the unit tests. The last line must say OK
python manage.py runserver           # then open http://127.0.0.1:8000/
```

Demo logins created by `seed_demo` (password for both: `campushub123`):

| Login | Who | Use it to show |
| --- | --- | --- |
| `sally@example.edu` | Student (persona Sally) | Planner, calendar, classes, settings |
| `jodi@example.edu` | Administrator (persona Jodi) | The **Admin** page: search and delete students |

Try the daily email: `python manage.py send_reminders`. The email is **printed in the terminal**
(nothing is really sent) because `config/settings.py` uses the "console" email backend.

---

## 2. The big idea: one class per file, grouped by job

```
planner/
├── models/         WHAT we store. One class per file: Student, Course, Item, RepeatingEvent...
├── factories/      FACTORY METHOD pattern. One "creator" class per item type.
├── commands/       COMMAND pattern. One class per user action (add, edit, delete...).
├── services/       Helpers that are not tables or pages: ItemFilter, WeekCalendar, email.
├── controllers/    Handle a web request and send a page back (UML diagram CD-5).
├── templates/      The HTML pages.
├── static/         campus_hub.css: our own look on top of Bootstrap.
├── tests/          Unit tests, one file per step below.
├── management/     Extra manage.py jobs: send_reminders, seed_demo.
├── migrations/     Django's record of the database layout (generated, but committed to Git).
├── form_tools.py   Turns form text ("2026-11-20") into dates and back.
└── urls.py         Which web address runs which controller function.
```

How one click travels through the code (example: saving the "Add item" form):

```
Browser
  → urls.py                       finds the function for /items/add/
  → controllers/item_controller   add_item(): builds an AddItemCommand, gives it to the invoker
  → commands/invoker              CommandInvoker.run(): calls command.execute()
  → commands/add_item             AddItemCommand.execute(): asks the factory for the right creator
  → factories/assignment          AssignmentCreator.make_item(): builds the Item
  → models/item                   Item.validate(), then save() into the database
  ← controller                    shows the list again with "Added ... [Undo]"
```

**Why this layout lets four people work at once:** each person adds *new files*. The only
shared files are a few short "hook" files where you add one or two lines (listed in
section 5). Small edits in different places merge cleanly in Git.

---

## 3. The two design patterns

### Factory Method (creational). Folder: `planner/factories/`

| Pattern role | Our class | File |
| --- | --- | --- |
| Creator (abstract) | `ItemCreator` | `factories/base.py` |
| Factory method | `make_item()` | declared in `base.py`, written in each subclass |
| Concrete creators | `AssignmentCreator`, `TestQuizCreator`, `ProjectCreator`, `MeetingCreator`, `ClassSessionCreator`, `JobShiftCreator`, `ClubMeetingCreator`, `OtherCreator` | one file each |
| Product | `Item` | `models/item.py` |
| Registry (replaces if/else) | `get_creator()`, `all_creators()` | `factories/registry.py` |

- **Problem it solves:** without it, "add item" is one long `if type == ... elif ...` block
  that everybody has to edit for every new type.
- **What we gained:** a new item type is one new file plus two lines. The forms, list,
  filters, calendar and email all pick it up automatically.
- **Tradeoff:** more small classes, and you step through two classes when debugging.
- **Honest design note:** the textbook version returns a different product *subclass* per
  creator. Our UML (CD-2) has one `Item` class with a `type`, so each creator returns an
  `Item` set up for its type (defaults such as an 11:59 PM due time, plus its own rules in
  `extra_errors()`). Same pattern, one database table.

### Command (behavioral). Folder: `planner/commands/`

| Pattern role | Our class | File |
| --- | --- | --- |
| Command (abstract) | `Command` with `execute()` and `undo()` | `commands/base.py` |
| Concrete commands | `AddItemCommand`, `EditItemCommand`, `DeleteItemCommand`, `MarkCompleteCommand`, `DeleteSelectedCommand`, `AddCourseCommand`, `DropCourseCommand`, `AddRepeatingEventCommand`, `EditRepeatingEventCommand`, `DeleteRepeatingEventCommand` | one file each |
| Invoker | `CommandInvoker` (`run()`, `undo_last()`) | `commands/invoker.py` |
| Receiver | the model objects (`Item`, `Course`, `RepeatingEvent`) | `models/` |
| Client | the controller functions | `controllers/` |

- **Problem it solves:** the page code no longer contains the logic, so pages can change
  without breaking behaviour.
- **What we gained:** an **Undo** button (add, edit, delete, complete, delete-many), and
  "delete several at once" is built out of single delete commands (a macro command).
- **Tradeoff:** more classes than writing the logic straight in the view.
- **Where the two patterns meet:** `commands/add_item.py`. It contains no `if` on the item type.

---

## 4. The steps (work packages)

Each step is a group of classes that belong together, with its own test file. The steps
are in dependency order: a step only uses things from earlier steps. **Each step is one
Git commit**, and the app runs and passes all of its tests after every one of them.

| Step | Adds | Classes / files | Stories and use cases | Test file |
| --- | --- | --- | --- | --- |
| 1 | Foundation and the data models | all of `models/` (`Student`, `Administrator`, `Course`, `ItemType`, `Item`, `RepeatingEvent`), `migrations/0001_initial.py`, `admin.py`, `form_tools.py`, `controllers/home_controller.py`, `controllers/helpers.py`, `urls.py`, `base.html`, `welcome.html`, `campus_hub.css`, settings additions | UML CD-1, CD-2 | `test_step01_foundation.py` |
| 2 | Accounts | `controllers/account_controller.py`, `signup.html`, `login.html` | US-01, US-02 / UC-01, UC-02 | `test_step02_accounts.py` |
| 3 | **Command** pattern base + classes and activities | `commands/base.py` (`Command`), `commands/invoker.py` (`CommandInvoker`), `commands/registry.py`, `commands/add_course.py`, `commands/drop_course.py`, `controllers/course_controller.py`, `course_*.html` | UC-09, UC-10 | `test_step03_courses.py` |
| 4 | **Factory Method** pattern + add an item + the main list | `factories/base.py` (`ItemCreator`), `factories/registry.py`, `factories/assignment.py`, `commands/add_item.py`, `controllers/item_controller.py` (`show_list`, `add_item`), `item_list.html`, `item_form.html`, `_item_badges.html` | US-05 / UC-03 | `test_step04_factory.py` |
| 5 | The other item types (one file each: easy to share out) | `factories/test_quiz.py`, `project.py`, `meeting.py`, `class_session.py`, `job_shift.py`, `club_meeting.py`, `other.py` | US-05, US-06 types | `test_step05_item_types.py` |
| 6 | Item actions: edit, delete, complete, delete many, undo | `commands/edit_item.py`, `delete_item.py`, `mark_complete.py`, `delete_selected.py`, more functions in `item_controller.py`, `item_confirm_delete.html` | US-04, US-07, US-08 / UC-05 to UC-08 | `test_step06_commands.py` |
| 7 | Filters | `services/item_filter.py` (`ItemFilter`), filter bar in `item_list.html` | US-03, US-09 / UC-11, UC-12 | `test_step07_filter.py` |
| 8 | Weekly calendar + item details page | `services/week_calendar.py` (`WeekCalendar`), `controllers/calendar_controller.py`, `calendar_week.html`, `item_detail.html` | US-13 / UC-13 | `test_step08_calendar.py` |
| 9 | Repeating events | `commands/add_repeating_event.py`, `edit_repeating_event.py`, `delete_repeating_event.py`, `controllers/event_controller.py`, `event_form.html`, `event_detail.html` | US-06, US-07 / UC-04 | `test_step09_repeating_events.py` |
| 10 | Daily reminder email + settings switch | `services/email_service.py` (`EmailService`), `services/daily_reminder_job.py` (`DailyReminderJob`), `management/commands/send_reminders.py`, `controllers/settings_controller.py`, `settings.html` | US-10, US-11 / UC-14, UC-15 | `test_step10_reminders.py` |
| 11 | Administrator deletes a student | `controllers/admin_controller.py`, `admin_students.html`, `admin_confirm_delete.html` | US-12 / UC-16 | `test_step11_admin.py` |
| 12 | Demo data and this guide | `management/commands/seed_demo.py`, `docs/design/BUILD_PLAN.md`, `README.md` | for the presentation | — |

**Why the data models all arrive in step 1:** they point at each other (an `Item` has a
`Course`, a `Course` has an owner `Student`), so they need to exist together. It also means
the whole project needs only one database migration. Everything after step 1 adds
*behaviour* (patterns, pages, helpers) without touching the database layout.

One way to split the work between four people so nobody edits the same files:
**A:** steps 1, 2, 11 (models, accounts, admin) · **B:** steps 4, 5 (items and the Factory) ·
**C:** steps 3, 6, 7 (Commands and filters) · **D:** steps 8, 9, 10 (calendar, repeating events, email).

### Walking through the steps in Git

The steps are commits on the branch `feature/campus-hub-app`, and each one has a tag
(`step-01` to `step-12`) so you can jump to it by name.

```
git log --oneline                 # see the 12 step commits, newest first
git show --stat step-04           # which files step 4 added or changed
git diff step-05 step-06          # exactly what step 6 changed
git switch --detach step-04       # look at (and run!) the project as it was after step 4
python manage.py test             # that step's tests
git switch feature/campus-hub-app # come back to the latest version
```

Good ways to use this: each teammate reads the commit(s) for the steps they own and can
explain them in the presentation, or retypes one step on a practice branch to learn it.
In the shared files (`urls.py`, `commands/__init__.py`, `factories/__init__.py`,
`base.html`, `item_list.html`) you can see each step add only its own block.

---

## 5. How to add something new without breaking anything

### The workflow (every time)

```
git switch main
git pull                                  # get the latest team code
git switch -c feature/internship-type     # your own branch
... add your new file(s) and your test ...
python manage.py test                     # everything must say OK
git add .
git commit -m "Add internship deadline item type"
git push -u origin feature/internship-type
```
Then open a pull request on GitHub and ask a teammate to review it.

### The hook files (the only shared files you touch)

| You are adding | New file goes in | Add your line(s) to |
| --- | --- | --- |
| An item type | `planner/factories/` | `planner/factories/__init__.py` (2 lines) |
| An action (command) | `planner/commands/` | `planner/commands/__init__.py` (2 lines) |
| A database class (model) | `planner/models/` | `planner/models/__init__.py` (1 line), then `makemigrations` + `migrate` |
| A page | `planner/controllers/` + `planner/templates/planner/` | `planner/urls.py` (a `path(...)` line in your step's block, or a new block) |
| A menu link | — | `planner/templates/planner/base.html` (1 line) |
| Tests | `planner/tests/test_....py` | nothing: Django finds files named `test*.py` by itself |

### Recipe A: a new item type (about 10 minutes, no database change)

1. Copy `planner/factories/other.py` to `planner/factories/internship.py`.
2. In the copy, change the class name to `InternshipCreator`, and set
   `type_code = "INTERNSHIP"`, `label = "Internship deadline"`, an `icon` and a `color`.
3. Optional: add rules by writing `extra_errors(self, item)` (see `meeting.py`).
4. At the bottom of `planner/factories/__init__.py` add:
   ```python
   from .internship import InternshipCreator
   register(InternshipCreator)
   ```
5. Add a test to `planner/tests/test_step05_item_types.py`, then run `python manage.py test`.

The new type now appears in the Add form, the filter dropdown, the list, the calendar and
the reminder email. You edited zero lines of working code. That is the Factory pattern paying off.

### Recipe B: a new action (command)

1. Copy `planner/commands/mark_complete.py` to a new file, e.g. `duplicate_item.py`.
2. Rename the class, give it a new `name = "duplicate_item"`, and write `execute()`.
   Set `can_undo = True` only if you also write `undo()`.
3. Register it at the bottom of `planner/commands/__init__.py` (2 lines).
4. Write a test that runs it through `CommandInvoker({})` (see `test_step06_commands.py`).
5. To put it on a page: add a controller function, one `path(...)` line in `urls.py`, and a button.

### Safety rules that keep `main` working

- Never change what an existing method returns. Add a new method instead.
- Run **all** the tests before you push, not just your own.
- If you add or change a model field, commit the new file in `planner/migrations/` too,
  and tell the team to run `python manage.py migrate` after they pull.
- Never commit `db.sqlite3` or `.venv` (the `.gitignore` already blocks them).

---

## 6. Unit test plan

Run everything with `python manage.py test`. Django builds a temporary empty database for
the tests, so your real data is never touched.

| Test file | Unit under test | What is checked (examples) |
| --- | --- | --- |
| `test_step02_accounts.py` | `Student`, account pages | reminders default ON; password is hashed; duplicate email rejected; wrong password message; logout blocks the list |
| `test_step03_courses.py` | `Course`, `AddCourseCommand`, `DropCourseCommand` | name needed; dropping deletes its items only; can't drop another student's class |
| `test_step04_factory.py` | `Item`, `ItemCreator`, registry, `AddItemCommand` | validation; abstract class can't be created; default due time; every registered creator makes its own type; students only see their own items |
| `test_step05_item_types.py` | each concrete creator | the special rule of each type |
| `test_step06_commands.py` | `Command`, `CommandInvoker`, item commands | edit/delete/complete and their undo; delete many; undo works once; 404 on another student's item |
| `test_step07_filter.py` | `ItemFilter` | by class, by type, both, hide completed, clear |
| `test_step08_calendar.py` | `WeekCalendar` | week starts Sunday; next/previous; items on the right day; empty week message |
| `test_step09_repeating_events.py` | `RepeatingEvent` and its commands | right days inside the date range; validation; edit all; remove one date; delete all |
| `test_step10_reminders.py` | `DailyReminderJob`, `EmailService`, settings | 7-day list in order; "Hooray" email; OFF means no email; only own items; failed send |
| `test_step11_admin.py` | `Administrator`, admin pages | search; delete removes all data; can sign up again; students are blocked |

Techniques worth naming in the presentation: **arrange / act / assert**, a **fake**
(`FakeEmailService`) passed in by **dependency injection**, fixed dates passed as `today`
so tests give the same result every day, and Django's test client acting as a browser.

---

## 7. Where the code differs from our UML (update the diagrams or mention it)

| UML | Code | Why |
| --- | --- | --- |
| `User` abstract parent of `Student` and `Administrator` (CD-1) | `Student` *has a* Django `User`; `Administrator` wraps a staff `User` | Reuses Django's tested login and password hashing (NFR-03) |
| `Item` attributes (CD-2) | adds `end_time` | Meetings and job shifts have a length |
| `Course` attributes (CD-2) | adds `color` | Class colors on the list and calendar |
| `ItemType` enumeration | `ItemType` holds the names; label, icon and rules live in the creators | Lets a type be added in one file |
| `ItemController.addRepeatingEvent`, `editItem(..., justThisOne)` (CD-5) | separate `event_controller.py`; "just this one" is `DeleteRepeatingEventCommand` with `only_date` | Keeps the repeating-event work in its own files |
| `RepeatingEvent.updateOne(date, changes)` | not built yet | See section 8 |
| Controllers are classes | one file per controller, one function per method | Simplest Django style |
| Not in UML | `factories/` and `commands/` packages, `CommandInvoker` | Added for the design patterns assignment: add them to the class diagram |
| Use case text | reminder list also includes overdue items; main page has a "Due soon" banner | Helpful extras |

---

## 8. Ideas for next steps (not built yet)

Each one is a self-contained addition that follows the recipes above.

| Idea | What to add | Size |
| --- | --- | --- |
| Internship deadline type (persona Carl) | one creator file (Recipe A) | Small |
| Duplicate an item | `DuplicateItemCommand` (Recipe B) | Small |
| Priority (Low / Medium / High) | one field on `Item` + migration + badge | Small |
| Edit a class (rename, recolor) | `EditCourseCommand` using `Course.rename()` + form page | Small |
| Change just ONE date of a repeating event | `RepeatingEvent.update_one()` + command + form | Medium |
| Export my planner to a file | `ExportItemsCommand` | Medium |
| "Turn off reminders" link inside the email | signed link + controller function | Medium |
| GitHub Actions: run the tests on every pull request | `.github/workflows/tests.yml` | Small |
| Deploy for the demo (Render or PythonAnywhere) + real email + scheduler | settings + host setup | Medium |
