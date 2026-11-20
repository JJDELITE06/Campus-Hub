# UC-02 - Log in and log out

| Use Case – 02 | Log in and log out  (goes with US-02) |
|---|---|
| **Primary Actors** | Sally, Carl |
| **Flow of events** | 1. User goes to the login page.<br>2. User types in their email and password and clicks "Log In."<br>3. System checks that the email and password match an account.<br>4. System shows the user's main page with only their own items.<br>5. When the user is done, they click "Log Out."<br>6. System clears the session and goes back to the login page. |
| **System** | Class management web site |
| **Preconditions** | User already has an account (UC-01). |
| **Postconditions** | User is logged in and only sees their own items. After logging out, nobody can see their planner on that device without logging in again. |
| **Business Relevance** | Keeps each student's planner private so nobody else can log in to see it. |
| **Dependencies** | UC-01 |
| **Extensions** | 3a. Email or password is wrong: system shows "Email or password is incorrect" and the user can try again. |
| **Priorities** | Highest |
| **Nonfunctional requirements** | Logging in takes 3 seconds or less.<br>Works in supported browsers / platforms (phone, PC, Mac). |
