# 🌐 Endpoints - "Collaborators" API

➡️ [Back to the Technical Documentation Summary](../doc.md)

_This file describes the **API endpoints** of this API project._

## Users

`GET /users`

-   Retourne la liste des utilisateurs majeurs (≥ 18).
-   Filtre optionnel par équipe : GET /users?team=Ops.

`GET /stats`

-   Retourne : nombre total (après filtrage majeur), moyenne d’âge (1 décimale), et top 3 des plus âgés (nom + âge).
-   Filtre optionnel par équipe : GET /stats?team=Ops.
