"""
health.py

This module defines health check endpoints for the application,
including liveness and readiness probes, following common microservice
practices for monitoring and orchestration (e.g., Kubernetes).

Endpoints:
    /health/live  - Liveness check: indicates the service is running.
    /health/ready - Readiness check: verifies dependencies and logging are operational.
"""

from fastapi import APIRouter
from app.services.json_service import JSONService
from app.services.user_service import user_service
from app.services.logger_service import logger_service

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("/live")
async def alive():
    """_Liveness endpoint to indicate that the application is running._

    This endpoint should be lightweight and always return a successful response
    as long as the application process is alive.

    Returns:
        dict: A simple JSON response with HTTP-like status and message.

    Example Response:
        {
            "status": 200,
            "message": "alive"
        }
    """
    return {
        "status": 200,
        "message": "alive",
    }
@router.get("/ready")
async def ready():
    """_Readiness endpoint to verify that application dependencies are operational._

    Checks performed:
        - UserLoader can load users from the CSV.
        - JSONService can format a test payload.
        - LoggerService can write a test log message.

    If any check fails, an error list is returned and HTTP status-like code is set to 503.
    Otherwise, the service is considered ready.

    Returns:
        dict: JSON response indicating readiness status, optional errors if not ready.

    Example Ready Response:
        {
            "status": 200,
            "message": "ready"
        }

    Example Not Ready Response:
        {
            "status": "503",
            "message": "not ready",
            "errors": [
                "UserLoader error: ..."
            ]
        }
    """
    errors = []

    try:
        user_service.get_users()
    except (ValueError, TypeError, RuntimeError) as e:
        errors.append("UserService error: %s", e)

    try:
        JSONService.format({"test": 123})
    except (ValueError, TypeError) as e:
        errors.append("JSONService error: %s", e)

    is_log_working = True
    try:
        logger_service.info("HTTP Request - Readiness - Test Logging")
    except (ValueError, TypeError, RuntimeError, OSError) as e:
        errors.append("LoggerService error: %s", e)
        is_log_working = False

    if errors:
        if is_log_working:
            logger_service.error("HTTP Request - Readiness check failed: %s", errors)
            return {
                "status": "503",
                "message": "not ready",
                "errors": errors
            }
    logger_service.info("HTTP Request - Readiness - Everything OK")
    return JSONService.format(message="ready")
