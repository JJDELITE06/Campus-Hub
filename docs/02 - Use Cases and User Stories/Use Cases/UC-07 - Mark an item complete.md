# UC-07 - Mark an item complete

| Use Case – 07 | Mark an item complete  (goes with US-08) |
|---|---|
| **Primary Actors** | Sally, Carl |
| **Flow of events** | 1. User selects an item to mark it as complete.<br>2. System marks the item as done and moves it to the Completed section.<br>3. User can still see the item in the Completed section. |
| **System** | Class management web site |
| **Preconditions** | User is logged in and has at least one item that is not done. |
| **Postconditions** | The item shows as done in the Completed section. |
| **Business Relevance** | Students can see what they have already finished and what is still left to do. |
| **Dependencies** | UC-03 |
| **Extensions** | 1a. User "uncompletes" an item in the Completed section: system moves it back to the not-done section. |
| **Priorities** | High |
| **Nonfunctional requirements** | The item moves within 1 second after it is marked complete.<br>Works in supported browsers / platforms (phone, PC, Mac). |
