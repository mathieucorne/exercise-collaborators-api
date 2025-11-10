"""_main.py_

Main module and entrypoint of the API.

This module initializes the FastAPI application, sets up the application
lifespan, loads initial user data via UserService, and includes all routers
for users, stats, and health endpoints.

It also provides a simple root endpoint for basic connectivity checks.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from app.routers import users, stats, health
from app.services.user_service import user_service
from app.services.json_service import JSONService

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """_Application lifespan context manager._

    This function is executed on application startup and shutdown.
    During startup, it refreshes user data from the CSV using the
    singleton UserService, ensuring in-memory data is ready for requests.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    user_service.refresh_users_data()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(stats.router)
app.include_router(health.router)

router = APIRouter()

@router.get("/")
def hello_world():
    """_Root endpoint to verify API connectivity._

    Returns:
        dict: JSON response with a welcome message.

    Example Response:
        {
            "status": 200,
            "message": "Hello World, you're using API Collaborators"
        }
    """
    return JSONService.format(message="Hello World, you're using API Collaborators")

app.include_router(router)
