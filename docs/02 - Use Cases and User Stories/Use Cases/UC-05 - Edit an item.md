# UC-05 - Edit an item

| Use Case – 05 | Edit an item  (goes with US-07) |
|---|---|
| **Primary Actors** | Sally, Carl |
| **Flow of events** | 1. User clicks "Edit" on an item.<br>2. System shows the form with the current information already filled in.<br>3. User changes something (like a meeting time or due date) and clicks "Save."<br>4. System checks the information (same checks as UC-03).<br>5. System saves the change and shows the updated item in the list, on the calendar, and in every other view. |
| **System** | Class management web site |
| **Preconditions** | User is logged in and the item already exists. |
| **Postconditions** | The item is updated everywhere it shows up. |
| **Business Relevance** | Due dates and meeting times change, for example when a professor gives an extension. |
| **Dependencies** | UC-03, UC-04 |
| **Extensions** | 1a. The item is a repeating event: system asks "Change just this one or all of them?" and only changes what the user picked.<br>3a. User clicks "Cancel": nothing changes. |
| **Priorities** | High |
| **Nonfunctional requirements** | The change shows up within 2 seconds after clicking Save.<br>Works in supported browsers / platforms (phone, PC, Mac). |
