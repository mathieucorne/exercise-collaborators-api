"""
users_router.py

This module defines the /users endpoints for the application.

It provides access to the list of users, optionally filtered by team,
and supports refreshing the in-memory user data from the data source
(UserLoader via UserService).

Endpoints:
    /users/        - Retrieve users, optionally filtered by team.
    /users/refresh - Reloads user data from the data source.
"""

from fastapi import APIRouter
from app.models.user import User
from app.services.json_service import JSONService
from app.services.user_service import user_service
from app.services.logger_service import logger_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
async def read_users(team : str = None):
    """
    Retrieve a list of users, optionally filtered by team.

    Args:
        team (str | None): Optional team name to filter users. If None,
                           all users are returned.

    Returns:
        dict: JSON response containing:
            - data (List[User]): List of users (optionally filtered by team)
            - status (int): HTTP-like status code
            - message (str): Status message

    Behavior:
        - If no users are loaded, returns status 422 with a warning.
        - Logs request and success using LoggerService.

    Example Response:
        {
            "status": 200,
            "message": "Getting Users Data",
            "data": [
                {"name": "Alice", "age": 30, "team": "Backend", ...},
                {"name": "Bob", "age": 25, "team": "Frontend", ...}
            ]
        }
    """
    users : list[User] = user_service.get_adult_users()
    if len(users) == 0:
        logger_service.warning("HTTP Request - get_stats: No Users Data Available")
        return JSONService.format(status=422, message="No Users Data Available")
    if team is not None :
        users_result : list[User] = user_service.get_users_of_team_of(users, team)
    else:
        users_result = users
    logger_service.info("HTTP Request - get_users : success")
    return JSONService.format(data=users_result, message="Getting Users Data")

@router.get("/refresh")
async def refresh_users():
    """
    Refresh the in-memory user data by reloading from the data source.

    Returns:
        dict: JSON response indicating that user data has been refreshed.

    Behavior:
        - Calls UserService.refresh_users_data to reload users from the CSV.
        - Logs the refresh action using LoggerService.

    Example Response:
        {
            "status": 200,
            "message": "Refreshing Users Data"
        }
    """
    logger_service.info("HTTP Request - Refreshing Users Data : success")
    user_service.refresh_users_data()
    return JSONService.format(message="Refreshing Users Data")
