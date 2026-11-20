# 01 - Software Requirements Spec

## Campus Hub - Team 5





## Introduction

This is Campus Hub App software requirements specification for Sacred Heart University, CS-312, Team 5

**The Problem** - Students track assignments, tests, meetings, job shifts and club activities across their syllabus, Blackboard, email and group chats. Deadlines get missed because nothing shows everything in one place. Deadlines change and information comes in from all angles.

**The Goal of Campus Hub** - One place where a student records every deadline and commitment, sees what is coming up in date order and on a weekly calendar, and is reminded by email before things are due.



## Users (Personas)

There are three kinds of people (personas, actors) that  are going to use Campus Hub.

1. On campus student who has maybe some club meetings, classes, tests, etc.
2. Off campus student who has similar classes but could have off campus job etc.
3. The administrator of Campus Hub who has to fix problems and deal with users who should not be there.



## Functional Requirements

| FR ID Num | Requirement                                                  | Use Case | User Story |
| --------- | ------------------------------------------------------------ | -------- | ---------- |
| FR-01     | The user should be able to make an account with their name, email and a password. The email can't already be used and the password has to be at least 8 characters. | UC-01    | US-01      |
| FR-02     | The user should be able to log in with their email and password and log out when they are done. Nobody else should be able to see their planner. | UC-02    | US-02      |
| FR-03     | The user should be able to add an item like an assignment, test, project or meeting. It needs a title and a due date. | UC-03    | US-05      |
| FR-04     | The user should be able to add something that repeats, like a class, club meeting or job shift, so they don't have to type it in every week. | UC-04    | US-06      |
| FR-05     | The user should be able to change an item, like the due date or time, and then save it or cancel. | UC-05    | US-07      |
| FR-06     | The user should be able to delete an item they don't need anymore. The app asks "are you sure?" first. | UC-06    | US-04      |
| FR-07     | The user should be able to mark an item as done. It stays in the list so they can see they finished it. | UC-07    | US-08      |
| FR-08     | The user should be able to pick a bunch of finished items and delete them all at once. | UC-08    | US-04      |
| FR-09     | The user should be able to add a class or activity with a name, a color and a class code if it has one (like CS312). | UC-09    | none       |
| FR-10     | The user should be able to drop a class. The app warns them that all the items for that class will get deleted too. | UC-10    | none       |
| FR-11     | The user should be able to filter the list so it only shows one class or activity at a time, or pick "All" to see everything. | UC-11    | US-03      |
| FR-12     | The user should be able to filter the list by type, like only tests or only job shifts, or pick "All". | UC-12    | US-09      |
| FR-13     | The user should be able to see a weekly calendar with all their stuff on the right days and go to the next or last week. | UC-13    | US-13      |
| FR-14     | The app should send the user an email every morning with everything due that week, in order by date. | UC-14    | US-10      |
| FR-15     | The user should be able to turn the daily email on or off. It is on when you first make your account. | UC-15    | US-11      |
| FR-16     | The admin should be able to delete a user and all of their stuff. | UC-16    | US-12      |





## Nonfunctional Requirements

| NFR ID Num | Type             | Requirement                                                  |
| ---------- | ---------------- | ------------------------------------------------------------ |
| NFR-01     | Speed            | Pages like the list and the calendar should load in 3 seconds or less. Logging in should take less than 3 seconds. |
| NFR-02     | Speed            | When you save, change or finish an item it should show up in 2 seconds or less. |
| NFR-03     | Security         | Passwords should not be saved as plain text. They should be hashed. |
| NFR-04     | Security         | A student can only see and change their own stuff, never somebody else's. |
| NFR-05     | Security         | Only the admin can get to the admin pages.                   |
| NFR-06     | Works everywhere | The app should work on iPhone, Android, and on Windows and Mac computers in the normal browsers. You shouldn't have to scroll sideways on a phone. |
| NFR-07     | Saving data      | Nothing should get lost if you close the browser or the server restarts. |
| NFR-08     | Easy to use      | Someone who never used the app should be able to add a class and an assignment in under 2 minutes without help. |
| NFR-09     | Easy to use      | At least two people on the team should check the screens against the inclusivity heuristics from class. |
| NFR-10     | Accessibility    | You should be able to fill out every form with just the keyboard, and the buttons should be big enough to tap on a phone. |
| NFR-11     | Reliability      | The reminder emails should go out before 7 AM. If one email fails, the rest should still go out. |
| NFR-12     | Testing          | We should have automated tests for most of the back-end code (at least 70%), and they all need to pass before we merge code. |
| NFR-13     | Easy to change   | It should be easy to add a new item type later without rewriting code that already works. |
| NFR-14     | Technology       | We will build it with Python, Django, SQLite and Bootstrap. It's a website, not a phone app. |
| NFR-15     | Process          | All the code goes in our GitHub repo, and every change needs a pull request that someone else on the team looks at. |
| NFR-16     | Security         | The email password for sending reminders should not be put in GitHub. |

