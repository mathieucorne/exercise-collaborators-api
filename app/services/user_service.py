""" _user_service.py_

This module provides the UserService class, which acts as a singleton responsible
for managing in-memory user data. It loads user records from the data source 
(UserLoader) and provides convenient methods to filter and analyze user data.
"""

import heapq
from app.models.user import User
from app.services.user_loader import UserLoader

class UserService:
    """_Singleton service class that manages user data loaded from external sources._

    This class maintains the list of users in memory, allows refreshing the data,
    and provides convenient access and filtering methods.

    Attributes:
        _instance (UserService): Singleton instance of the class.
        users (list[User]): In-memory list of user objects.
    """
    _instance: "UserService" = None
    def __new__(cls):
        """_Ensures only one instance of the class exists (Singleton pattern).

        Returns:
            UserService: The single instance of the UserService class.
        """
        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance = instance
        return cls._instance
    def __init__(self):
        """_Initializes the UserService instance._

        This method sets up the internal list of users.
        If the singleton instance already exists, this constructor
        does not reinitialize the data.
        """
        self.users = []
    def refresh_users_data(self) -> None:
        """_Reloads user data from the data source (CSV file via UserLoader)._

        This method replaces the current in-memory list of users with
        a newly loaded list.
        """
        self.users = UserLoader.load_users_from_file()
    def get_users(self) -> list[User]:
        """_Retrieves the current in-memory list of users._

        Returns:
            list[User]: A list of User model instances currently loaded in memory.
        """
        return self.users
    @staticmethod
    def get_users_of_team_of(users_data : list[User], team) -> list[User]:
        """_Filters a list of users by team._

        Args:
            users_data (List[User]): The list of users to filter.
            team (str | None): The team name to filter by. If None, returns all users.

        Returns:
            List[User]: List of users belonging to the specified team.
        """
        users_result : list[User] = []
        for user in users_data:
            if (team is None or user.team == team):
                users_result.append(user)
        return users_result
    @staticmethod
    def get_average_age_of(users_data : list[User]) -> float:
        """_Calculates the average age of a list of users._

        Args:
            users_data (List[User]): The list of users to calculate the average age for.

        Returns:
            float: The average age of the users. Returns 0.0 if the list is empty.
        """
        nb_users = 0
        average_age : float = 0.0
        for user in users_data:
            nb_users+=1
            average_age+=user.age
        return round(average_age = average_age / nb_users, 1)
    @staticmethod
    def get_n_oldest_users(users_data : list[User], n : int) -> list[User]:
        """_Returns the N oldest users from a list._

        Args:
            users_data (List[User]): The list of users to select from.
            n (int): The number of oldest users to return.

        Returns:
            List[User]: The N oldest users, sorted by descending age.
        """
        heapq.nlargest(n,users_data, key=lambda u: u.age)
# Global singleton instance accessible throughout the application
user_service = UserService()
