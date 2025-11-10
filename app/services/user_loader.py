"""_user_loader.py_

This module provides the UserLoader class, responsible for loading and parsing
user data from a CSV file. It transforms raw CSV rows into validated User objects
and logs any issues encountered during parsing.
"""
# pylint: disable=too-few-public-methods

import os
from csv import DictReader
from app.models.user import User
from app.services.logger_service import logger_service

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "users.csv")
USER_CSV_FIELDS = ["name", "email", "age", "team", "start_date"]

class UserLoader:
    """_A stateless utility class responsible for reading user data from a CSV file._

    The class contains only static methods, meaning it does not maintain any internal
    state or instance data. It simply loads data, validates it, and converts each row
    into a `User` model instance.

    Example:
        >>> users = UserLoader.load_users_from_file("path/to/users.csv")
        >>> for user in users:
        ...     print(user.name)
    """

    @staticmethod
    def load_users_from_file(file_path: str = CSV_PATH) -> list[User]:
        """_Loads users from a CSV file and returns them as a list of `User` objects._

        This method validates the CSV header, parses each row, and logs warnings for
        invalid rows. Only valid users are returned.

        Args:
            file_path (str): Optional path to the CSV file. Defaults to the global `CSV_PATH`.

        Returns:
            list[User]: A list of successfully parsed and validated `User` objects.

        Raises:
            ValueError: If the CSV header does not match the expected `USER_CSV_FIELDS`.
        """
        users = []
        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = DictReader(csvfile)
            if reader.fieldnames != USER_CSV_FIELDS:
                raise ValueError(
                    f"Invalid CSV header: expected {USER_CSV_FIELDS}, got {reader.fieldnames}")
            UserLoader._parse_user_rows(users, reader)
            logger_service.info("Users data loaded: %s valid users", len(users))
            return users

    @staticmethod
    def _parse_user_rows(users : list[User], reader : DictReader[str]) -> None:
        """_Parses individual rows from the CSV reader and appends valid users to the list._

        This method iterates through each CSV row, checks for missing or invalid data,
        and logs appropriate warnings for any issues. Valid rows are converted into
        `User` model instances and added to the provided list.

        Args:
            users (list[User]): The list where valid `User` objects will be appended.
            reader (csv.DictReader): The CSV reader object used to iterate through rows.

        Returns:
            None

        Logs:
            - Info: When a valid user is added.
            - Warning: When a row is skipped due to invalid or missing data.
        """
        for i_user_row, user_row in enumerate(reader, start=1):
            try:
                for field in USER_CSV_FIELDS:
                    if not user_row.get(field):
                        raise ValueError(f"Missing field '{field}'")

                user_name = user_row["name"].strip()
                user_email = user_row["email"].strip()
                user_age = int(user_row["age"])
                user_team = user_row["team"].strip()
                user_start_date = user_row["start_date"].strip()

                user = User(
                    name=user_name,
                    email=user_email,
                    age=user_age,
                    team=user_team,
                    start_date=user_start_date)
                users.append(user)
                logger_service.info("Line %s - New User added : %s", i_user_row, user.name)
            except (ValueError, KeyError, TypeError) as e:
                logger_service.warning(
                    "Line %s - Skipping invalid user row %s: %s", 
                    i_user_row, user_row, e)
