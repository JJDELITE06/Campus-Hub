# UC-03 Campus-Hub Team 5

| Use Case – 03 | Add a single item  (goes with US-05) |
|---|---|
| **Primary Actors** | Sally, Carl |
| **Flow of events** | 1. User clicks "Add Item."<br>2. System shows a form with title, type (quiz, assignment, project, meeting, etc.), class or activity name, due date, time, location (a classroom, Teams meeting, or Blackboard), and notes.<br>3. User fills in the form and clicks "Save."<br>4. System checks that the title and due date are filled in.<br>5. System saves the item and shows it in the list and on the calendar. |
| **System** | Class management web site |
| **Preconditions** | User is logged in (UC-02). |
| **Postconditions** | The new item is saved and shows up in the list and on the calendar. |
| **Business Relevance** | Having every assignment, test, and meeting in one place is the main reason for the app. |
| **Dependencies** | UC-02 |
| **Extensions** | 3a. User clicks "Cancel": nothing is saved.<br>4a. Title or due date is missing: system shows an error message and does not save. |
| **Priorities** | Highest |
| **Nonfunctional requirements** | The new item shows up within 2 seconds after clicking Save.<br>Works in supported browsers / platforms (phone, PC, Mac). |
