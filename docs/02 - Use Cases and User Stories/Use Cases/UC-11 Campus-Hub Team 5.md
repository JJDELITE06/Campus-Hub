# UC-11 Campus-Hub Team 5

| Use Case – 11 | Filter by class or activity  (goes with US-03) |
|---|---|
| **Primary Actors** | Sally, Carl |
| **Flow of events** | 1. User opens the class/activity dropdown on the main page.<br>2. System shows a list of the user's classes and activities, plus "All."<br>3. User picks one class or activity.<br>4. System shows only the items for that class or activity, soonest due date first. |
| **System** | Class management web site |
| **Preconditions** | User is logged in and has items with a class or activity. |
| **Postconditions** | Only the chosen items show. Nothing is deleted. |
| **Business Relevance** | Helps students focus on specific classes or activities one at a time. |
| **Dependencies** | UC-03, UC-09 |
| **Extensions** | 3a. User picks "All": system shows all items again.<br>4a. There are no items for that class or activity: system shows "Nothing here." |
| **Priorities** | Medium |
| **Nonfunctional requirements** | The list updates within 2 seconds.<br>Works in supported browsers / platforms (phone, PC, Mac). |
