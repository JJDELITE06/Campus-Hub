# UC-16 - Delete a user account

| Use Case – 16 | Delete a user account  (goes with US-12) |
|---|---|
| **Primary Actors** | Jodi (system administrator) |
| **Flow of events** | 1. Jodi logs in to the admin page.<br>2. System shows a list of student users.<br>3. Jodi searches for or scrolls to a specific user.<br>4. Jodi chooses to delete that user.<br>5. System shows a confirmation box: "Are you sure?"<br>6. Jodi clicks "Yes."<br>7. System deletes the user and all their data. |
| **System** | Class management web site |
| **Preconditions** | Jodi has an admin account. |
| **Postconditions** | The user and all their data are gone, and that user can't log in anymore. |
| **Business Relevance** | IT needs a way to remove accounts that shouldn't be there or that a student asked to close. |
| **Dependencies** | UC-01 |
| **Extensions** | 1a. A regular student tries to open the admin page: system blocks them.<br>3a. No user matches the search: system shows "No user found."<br>6a. Jodi clicks "Cancel": nothing is deleted. |
| **Priorities** | Medium |
| **Nonfunctional requirements** | Only admins can get to the admin page.<br>Works in supported browsers / platforms (phone, PC, Mac).<br>We can probably use the built-in Django admin page for most of this. |
