"""
user.py

This module defines the User Pydantic model, representing a user in the system.
The model enforces type validation and constraints on the user attributes.
"""

from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    """_Represents a user in the system._

    This model validates user data and ensures type safety. It can be used
    throughout the application wherever user information is required, such
    as in services, APIs, and data processing.

    Attributes:
        name (str): Full name of the user.
        email (EmailStr): User's email address, must be a valid email format.
        age (int): User's age, must be greater than or equal to 0.
        team (str): Name of the team the user belongs to.
        start_date (str): User's start date in YYYY-MM-DD format.
    
    Example:
        >>> user = User(
        ...     name="Alice Smith",
        ...     email="alice@example.com",
        ...     age=30,
        ...     team="Backend",
        ...     start_date="2024-09-01"
        ... )
        >>> print(user.name)
        Alice Smith
    """
    name: str
    email: EmailStr
    age: int = Field(..., ge=0)
    team: str
    start_date: str
