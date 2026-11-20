# UC-10 Campus-Hub Team 5

| Use Case – 10 | Drop a class  (from Student 2; no user story yet) |
|---|---|
| **Primary Actors** | Sally, Carl (the student wishing to delete the class) |
| **Flow of events** | 1. The user uses the UI to select the class they wish to delete.<br>2. The user selects the option to delete it.<br>3. System asks "Delete this class and all of its assignments?" and shows how many assignments will be deleted.<br>4. The user clicks "Yes."<br>5. That class and all its related assignments are gone from the website. |
| **System** | Class management web site |
| **Preconditions** | The user already has a class and some assignments on the site. |
| **Postconditions** | The class and all its related assignments are gone from the list, the calendar, and the dropdowns. Other classes and their assignments are not changed. |
| **Business Relevance** | A student drops a class and wants to delete it and all the related assignments from the website. |
| **Dependencies** | UC-06, UC-09 |
| **Extensions** | 4a. The user clicks "Cancel": nothing is deleted.<br>If things don't go smoothly (from Student 2):<br>&nbsp;&nbsp;&nbsp;&nbsp;- It could not allow the user to delete the class.<br>&nbsp;&nbsp;&nbsp;&nbsp;- It could say it deleted the class but it still shows up on the website.<br>&nbsp;&nbsp;&nbsp;&nbsp;- It could get rid of the class but all the pre-existing assignments stay.<br>(We should test for each of these.) |
| **Priorities** | Medium |
| **Nonfunctional requirements** | Deleting a class with up to 50 assignments takes 3 seconds or less.<br>Works in supported browsers / platforms (phone, PC, Mac). |
