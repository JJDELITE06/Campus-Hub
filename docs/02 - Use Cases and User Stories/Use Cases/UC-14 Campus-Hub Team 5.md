# UC-14 Campus-Hub Team 5

| Use Case – 14 | Send the daily reminder email  (goes with US-10) |
|---|---|
| **Primary Actors** | System (a timer that runs every day). Sally and Carl receive the email. |
| **Flow of events** | 1. Every morning before 7 AM Eastern, the timer starts the reminder job.<br>2. System finds every user who has reminder emails turned on.<br>3. For each user, system makes a list of items coming up in the next 7 days that are not yet done, in order of due date and time.<br>4. System emails the list to the user. Each item shows its name/title, type (class, job, etc.), and due date and time. |
| **System** | Class management web site |
| **Preconditions** | User has an account with an email address, and reminder emails are turned on. |
| **Postconditions** | Each user with reminders turned on gets one email for the day. |
| **Business Relevance** | A web app can't send notifications to a phone, so an email is how we remind students of what is coming up due, even when the app is closed. |
| **Dependencies** | UC-01, UC-03, UC-15 |
| **Extensions** | 3a. Nothing is due in the next 7 days: system sends a "Hooray, nothing is due!" email.<br>4a. The email doesn't send: system writes the error to a log and tries one more time later. |
| **Priorities** | Medium |
| **Nonfunctional requirements** | All emails are sent before 7 AM Eastern.<br>Each email only has that user's items. |
