# UC-09 - Add a new class

| Use Case – 09 | Add a new class  (from Student 2; no user story yet) |
|---|---|
| **Primary Actors** | Sally, Carl (the student wishing to add the class) |
| **Flow of events** | 1. The user uses the UI to go to "My Classes" and clicks "Add Class."<br>2. System shows a form for the class name and class code (for example CS312).<br>3. The user fills in the form and clicks "Save."<br>4. System saves the new class and it shows up in the class list and the class dropdown.<br>5. The user adds the class's assignments (UC-03), and the class shows up after with all their assignments there. |
| **System** | Class management web site |
| **Preconditions** | The user already has some classes on the site but wants to add another. |
| **Postconditions** | The new class shows up on the site, and all their assignments for it are there. |
| **Business Relevance** | A student adds a new class to their schedule after the semester starts and wants to add it to the website as well. |
| **Dependencies** | UC-02, UC-03 |
| **Extensions** | 3a. The class name is empty: system shows an error message and does not save.<br>3b. The user already has a class with that name: system shows "You already have this class."<br>If things don't go smoothly (from Student 2):<br>&nbsp;&nbsp;&nbsp;&nbsp;- It could not allow the user to add a new class.<br>&nbsp;&nbsp;&nbsp;&nbsp;- It could say the class was added but it doesn't show up.<br>&nbsp;&nbsp;&nbsp;&nbsp;- It could not be able to handle adding a new class after the semester already started.<br>(We should test for each of these.) |
| **Priorities** | High |
| **Nonfunctional requirements** | The new class shows up within 2 seconds after clicking Save.<br>A class can be added at any time during the semester, not just at the start.<br>Works in supported browsers / platforms (phone, PC, Mac). |
