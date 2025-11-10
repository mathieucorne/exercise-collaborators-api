"""_stats.py_

This module defines the /stats endpoints for the application. 

It provides aggregated statistics on users, including:
    - Total number of users
    - Number of users in a specific team
    - Average age of users
    - Top N oldest users

The endpoint leverages the UserService singleton for in-memory
user data and JSONService for consistent response formatting.
"""

from fastapi import APIRouter
from app.services.user_service import user_service
from app.models.user import User
from app.services.json_service import JSONService
from app.services.logger_service import logger_service

router = APIRouter(
    prefix="/stats",
    tags=["stats"]
)

@router.get("/")
async def get_stats(team: str = None):
    """
    Retrieve aggregated user statistics, optionally filtered by team.

    Args:
        team (str | None): Optional team name to filter users. If None,
                           statistics are computed across all users.

    Returns:
        dict: JSON response containing the following keys:
            - totalUsers (int): Total number of users in memory.
            - countedUsers (int): Number of users considered for statistics.
            - averageAgeOfUsers (float): Average age of considered users.
            - oldestUsers (List[User]): Top 3 oldest users.
            - status (int): HTTP-like status code.
            - message (str): Optional status message.

    Behavior:
        - If no users are loaded, returns a 422 status with a warning.
        - Otherwise, returns statistics for all users or filtered by team.
        - Logs requests and results using LoggerService.

    Example Response:
        {
            "status": 200,
            "message": "success",
            "data": {
                "totalUsers": 10,
                "countedUsers": 5,
                "averageAgeOfUsers": 29.4,
                "oldestUsers": [
                    {"name": "Alice", "age": 45, ...},
                    {"name": "Bob", "age": 42, ...},
                    {"name": "Carol", "age": 39, ...}
                ]
            }
        }
    """
    users : list[User] = user_service.get_users()
    total_users = len(users)
    if len(users) == 0:
        logger_service.warning("HTTP Request - get_stats: No Users Data Available")
        return JSONService.format(
            status = 422,
            data={"totalUsers": total_users},
            message="No Users Data Available"
        )
    if team is not None :
        users_result : list[User] = user_service.get_users_of_team_of(users, team)
    else:
        users_result = users
    average_age : float = user_service.get_average_age_of(users_result)
    oldest_users : list[User] = user_service.get_n_oldest_users(users_result, 3)
    logger_service.info("HTTP Request - get_stats: success")
    return JSONService.format(data={
        "totalUsers": total_users,
        "countedUsers": len(users_result),
        "averageAgeOfUsers": average_age,
        "oldestUsers": oldest_users
    })
