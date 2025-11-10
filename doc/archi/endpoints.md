# 🌐 Endpoints - "Collaborators" API

➡️ [Back to the Technical Documentation Summary](../doc.md)

_This file describes the **API endpoints** of this project._

## Users

`GET /users`

-   Returns the list of adult users (age ≥ 18).
-   Optional team filter: `GET /users?team=Ops`.

`GET /users/refresh`

-   Reloads the in-memory user data from the data source (CSV).
-   Useful to refresh data without restarting the application.

## Stats

`GET /stats`

-   Returns statistics about users: total number of adult users (after filtering), average age (1 decimal), and the top 3 oldest users (name + age).
-   Optional team filter: `GET /stats?team=Ops`.
