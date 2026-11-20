# UC-13 - View the weekly calendar

| Use Case – 13 | View the weekly calendar  (goes with US-13) |
|---|---|
| **Primary Actors** | Sally, Carl |
| **Flow of events** | 1. User clicks "Calendar."<br>2. System shows the current week (Monday to Sunday) with each item on the day it is due.<br>3. User clicks the forward or back button.<br>4. System shows the next or the previous week.<br>5. User clicks on an item.<br>6. System opens the item and shows its details. |
| **System** | Class management web site |
| **Preconditions** | User is logged in (UC-02). |
| **Postconditions** | Nothing is changed. The calendar is only for looking. |
| **Business Relevance** | Seeing the whole week helps students see how much is due on one day and notice busy days early. |
| **Dependencies** | UC-03, UC-04 |
| **Extensions** | 2a. Nothing is due that week: system shows the empty week with "Nothing due this week." |
| **Priorities** | Medium |
| **Nonfunctional requirements** | The calendar loads within 3 seconds.<br>It can be read on a phone screen without zooming.<br>Works in supported browsers / platforms (phone, PC, Mac). |
