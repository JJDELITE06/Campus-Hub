# US-12: Campus-Hub Team 5

## User story

As a system administrator (Jodi), I want to delete a user's account so that I can remove accounts that shouldn't be there or that a student asked to close.

| Field | Value |
|---|---|
| Priority | Low   (We can probably use the built-in Django admin page for most of this.) |
| Sprint # | TBD |
| Story Points | To be agreed in Planning Poker |

## Acceptance criteria

- Only admins can see the admin page. Regular students can't get to it.
- The admin can search for a user by email.
- Given the admin clicks Delete on a user, when they confirm, then the user and all of their items are deleted.
- After being deleted, that user can't log in anymore.

Definition of Done: see [Definition of Done - Common.md](Definition%20of%20Done%20-%20Common.md)
