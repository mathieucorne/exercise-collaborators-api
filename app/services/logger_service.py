"""_logger_service.py_

This module provides the LoggerService class, which configures and returns
a singleton logger instance for the application. The logger uses a
RotatingFileHandler to manage log files efficiently.
"""
# pylint: disable=too-few-public-methods

import logging
from logging.handlers import RotatingFileHandler

class LoggerService:
    """_Service class for creating and configuring a logger instance._

    This class provides a single static method to get a configured logger.
    The logger is set to INFO level and writes logs to a rotating file
    ('app.log'), with a maximum size of 1 MB per file and 5 backup files.

    Example:
        >>> from app.services.logger_service import LoggerService
        >>> logger = LoggerService.get_logger()
        >>> logger.info("This is an info message")
    """
    @staticmethod
    def get_logger():
        """_Returns a configured logger instance for the application._

        The logger is named "app", uses the INFO level, and writes logs
        to 'app.log' with rotation to avoid large files. If the logger
        already has handlers, it will not add duplicate handlers.

        Returns:
            logging.Logger: A configured logger instance.

        Example:
        ```
            >>> logger = LoggerService.get_logger()
            >>> logger.warning("This is a warning")
        ```
        """
        logger = logging.getLogger("app")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = RotatingFileHandler(filename="app.log", maxBytes=1_000_000, backupCount=5)
            formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
# Global logger instance accessible throughout the application
logger_service = LoggerService.get_logger()
