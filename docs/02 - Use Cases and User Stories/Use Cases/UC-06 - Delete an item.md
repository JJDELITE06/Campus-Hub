# UC-06 - Delete an item

| Use Case – 06 | Delete an item  (goes with US-04) |
|---|---|
| **Primary Actors** | Sally, Carl |
| **Flow of events** | 1. User clicks "Delete" on an item.<br>2. System asks "Do you really want to delete this?"<br>3. User clicks "Yes."<br>4. System deletes the item and removes it from the list and the calendar. |
| **System** | Class management web site |
| **Preconditions** | User is logged in and the item already exists. |
| **Postconditions** | The item is gone from the list and the calendar. |
| **Business Relevance** | Keeps the list from getting cluttered with things the student doesn't want any more. |
| **Dependencies** | UC-03 |
| **Extensions** | 1a. The item is a repeating event: system asks "Delete just this one or all of them?"<br>3a. User clicks "Cancel" because they changed their mind: nothing is deleted. |
| **Priorities** | High |
| **Nonfunctional requirements** | Works in supported browsers / platforms (phone, PC, Mac). |
