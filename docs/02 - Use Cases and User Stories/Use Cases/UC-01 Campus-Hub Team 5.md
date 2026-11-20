# UC-01 Campus-Hub Team 5

| Use Case – 01 | Create an account  (goes with US-01) |
|---|---|
| **Primary Actors** | Sally, Carl |
| **Flow of events** | 1. User clicks "Sign Up" on the home page.<br>2. System shows the sign-up form (name, email, password).<br>3. User submits a name, a valid email, and a password by clicking "Create Account."<br>4. System checks that every box is filled in and the email is not already used.<br>5. An account is created and the system shows the user's main page. |
| **System** | Class management web site |
| **Preconditions** | User navigated to sign-up page and does not have an account yet |
| **Postconditions** | Account is created and stored for future use |
| **Business Relevance** | Need for users to securely identify themselves to access their information |
| **Dependencies** | None |
| **Extensions** | 4a. A box is empty or the email is not valid: system shows an error message and keeps what the user already typed.<br>4b. The email already has an account: system shows "An account with this email already exists" and a link to log in. |
| **Priorities** | Highest |
| **Nonfunctional requirements** | Account is created and screen comes back within 5 seconds<br>Works in supported browsers / platforms (phone, PC, Mac).<br>The password is stored securely (hashed), not as plain text. |
