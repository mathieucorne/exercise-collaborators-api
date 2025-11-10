# 🚧 How to Resolve Errors in Services

➡️ [Back to the Technical Documentation Summary](../doc.md)

_This file describes **how to resolve errors in services** and provides technical documentation resources._

## Detecting errors in a Service

In this example, we wanted to ensure that the `data` attribute of the HTTP response returned by the `JSONService.format` method would **not appear** when no data is provided (i.e., `data=None`).

However, while testing the readiness endpoint (`/health/ready`), we observed an error in the logs:

```python
import json
from typing import Any

class JSONService():

    ...

    @staticmethod
    def format(data: Any | None = None, status: int = 200, message: str | None = None):
        return {
            "status": status,
            "message": message or "success",
            "data": data | None
        }
```

This happened because of a misuse of the || operator in Python (which is not valid, instead of `or` operator) when trying to fallback to None if the serialized data is not provided:

```python
"data": data || None
```

```json
{
    "status": "503",
    "message": "not ready",
    "errors": [
        "JSONService error: unsupported operand type(s) for |: 'str' and 'NoneType'"
    ]
}
```

## How the Error Was Detected

1. The **readiness probe** (`/health/ready`) is designed to check if all core services are operational:

-   UserService can load users.
-   JSONService.format works correctly.
-   LoggerService can write logs.

2. During the probe, the application tried to call `JSONService.format(data=None)` and failed.

3. The error was logged, causing the readiness check to return **503 Not Ready**, indicating that the service is not fully operational.

This is a perfect example of how **readiness probes can detect service misconfigurations or runtime errors** before exposing endpoints to production traffic.

## Resolution

To fix the issue, the `format` method should **conditionally include the `data` field only** if `data` is not `None`, without using invalid operators:

```python
import json
from typing import Any

class JSONService():

    ...

    @staticmethod
    def format(data: Any | None = None, status: int = 200, message: str | None = None):
        response = {
            "status": status,
            "message": message or "success",
        }
        if data is not None:
            response["data"] = data
        return response

```

Now, when data=None, the data attribute is simply omitted from the JSON response:

```json
{
    "status": 200,
    "message": "ready"
}
```

## Lessons Learned

-   **Readiness probes** are not only for orchestration; they help detect runtime issues with core services before clients experience them.

-   Always test utility methods (`JSONService.format`, `LoggerService`, etc.) with edge cases such as `None` values.

-   Avoid using non-Python operators (`||`) and prefer conditional logic for optional fields.
