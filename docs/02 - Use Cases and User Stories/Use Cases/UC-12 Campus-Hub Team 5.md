# UC-12 Campus-Hub Team 5

| Use Case – 12 | Filter by item type  (goes with US-09) |
|---|---|
| **Primary Actors** | Sally, Carl |
| **Flow of events** | 1. User opens the type dropdown on the main page.<br>2. System shows the types (assignment, test/quiz, project, class, job shift, club meeting, other), plus "All."<br>3. User picks a type.<br>4. System shows only the items of that type. |
| **System** | Class management web site |
| **Preconditions** | User is logged in and has items. |
| **Postconditions** | Only items of the chosen type show. Nothing is deleted. |
| **Business Relevance** | Lets a student focus on just one thing at a time. For example, Carl can see only his job shifts when planning his work week. |
| **Dependencies** | UC-03, UC-04 |
| **Extensions** | 3a. User picks "All": system shows all items again.<br>4a. There are no items of that type: system shows "Nothing here." |
| **Priorities** | High |
| **Nonfunctional requirements** | The list updates within 2 seconds.<br>Works in supported browsers / platforms (phone, PC, Mac). |
