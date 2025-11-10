"""_json_service.py_

This module provides the JSONService class, a stateless utility for
serializing Python objects to JSON strings and formatting standardized
JSON responses for API endpoints.
"""

import json
from typing import Any

class JSONService():
    """_A stateless utility service for JSON serialization and response formatting._

    This class provides static methods to:
        - Serialize Python objects into JSON strings.
        - Format data into a standard JSON response structure with status and message.

    Example:
        >>> from app.services.json_service import JSONService
        >>> data = {"name": "Alice", "age": 30}
        >>> json_str = JSONService.serialize(data)
        >>> response = JSONService.format(data=data, status=200, message="OK")
    """
    @staticmethod
    def serialize(obj: Any) -> str:
        """_Serializes a Python object into a JSON-formatted string._

        Args:
            obj (Any): The Python object to serialize.

        Returns:
            str: The JSON string representation of the object.

        Example:
            >>> JSONService.serialize({"name": "Alice"})
            '{"name": "Alice"}'
        """
        return json.dumps(obj)
    @staticmethod
    def format(data: Any | None = None, status: int = 200, message: str | None = None):
        """_Formats a standardized JSON response with status, message, and optional data._

        Args:
            data (Any | None): Optional payload data to include in the response.
            status (int): HTTP-like status code. Defaults to 200.
            message (str | None): Optional status message. Defaults to "success" if not provided.

        Returns:
            dict: A dictionary representing the structured JSON response.

        Example:
            >>> JSONService.format(data={"user": "Alice"}, status=201, message="Created")
            {
                "status": 201,
                "message": "Created",
                "data": {"user": "Alice"}
            }
        """
        response = {
            "status": status,
            "message": message or "success",
        }
        if data is not None:
            response["data"] = data
        return response
