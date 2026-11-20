# UC-08 Campus-Hub Team 5

| Use Case – 08 | Delete several completed assignments at once  (from Student 2; goes with US-04) |
|---|---|
| **Primary Actors** | Sally, Carl (the student wishing to delete the assignments) |
| **Flow of events** | 1. The user selects all the assignments they wish to delete (a checkbox next to each one, or a "Select all completed" button).<br>2. The user presses the delete button.<br>3. System asks "Do you really want to delete these assignments?" and shows how many are selected.<br>4. The user clicks "Yes."<br>5. The assignments all disappear from the site (the list and the calendar). |
| **System** | Class management web site |
| **Preconditions** | The user has multiple completed assignments to delete at once. |
| **Postconditions** | All the selected assignments are gone from the site. Assignments that were not selected are still there. |
| **Business Relevance** | A student does a bunch of late work they hadn't done yet in one sitting and wants to delete them all from the site. Deleting them one at a time would take too long. |
| **Dependencies** | UC-06, UC-07 |
| **Extensions** | 4a. The user clicks "Cancel": nothing is deleted.<br>5a. Some assignments can't be deleted because of an error: system shows an error message, says which ones were not deleted, and leaves them on the list.<br>If things don't go smoothly (from Student 2):<br>&nbsp;&nbsp;&nbsp;&nbsp;- It could not allow the user to select multiple assignments at once.<br>&nbsp;&nbsp;&nbsp;&nbsp;- It might not allow them to delete multiple assignments at once.<br>&nbsp;&nbsp;&nbsp;&nbsp;- It might not be able to handle deleting that many assignments at once.<br>&nbsp;&nbsp;&nbsp;&nbsp;- The assignments might not disappear after being deleted.<br>(We should test for each of these.) |
| **Priorities** | Medium |
| **Nonfunctional requirements** | Deleting up to 50 assignments at once takes 3 seconds or less.<br>Works in supported browsers / platforms (phone, PC, Mac). |
