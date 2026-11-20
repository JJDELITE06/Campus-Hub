# UC-04 - Add a repeating event

| Use Case – 04 | Add a repeating event  (goes with US-06) |
|---|---|
| **Primary Actors** | Sally, Carl |
| **Flow of events** | 1. User clicks "Add Repeating Event."<br>2. System shows a form with title, type (class, job shift, club meeting, etc.), days of the week (for example M, Th), start time, end time, first date, and last date.<br>3. User fills in the form and clicks "Save."<br>4. System checks that the boxes are filled in and the end time is after the start time.<br>5. System saves the event and shows it on every matching day on the calendar. |
| **System** | Class management web site |
| **Preconditions** | User is logged in (UC-02). |
| **Postconditions** | The event shows up on each chosen day between the first date and the last date. |
| **Business Relevance** | Students have classes, jobs, and clubs every week. Putting them in over and over again takes too long. |
| **Dependencies** | UC-02, UC-13 |
| **Extensions** | 4a. No days are picked, or the end time is before the start time: system shows an error message.<br>4b. No last date is entered: system asks for one (like the end of the semester) so the event doesn't repeat forever. |
| **Priorities** | Medium |
| **Nonfunctional requirements** | Saving an event that repeats for a whole semester (about 15 weeks) takes 3 seconds or less.<br>Works in supported browsers / platforms (phone, PC, Mac). |
