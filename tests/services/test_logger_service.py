import logging
from logging.handlers import RotatingFileHandler
from app.services.logger_service import LoggerService

def test_get_logger_returns_logger():
    logger = LoggerService.get_logger()
    assert isinstance(logger, logging.Logger)
    assert logger.name == "app"
    assert logger.level == logging.INFO

def test_logger_has_rotating_file_handler():
    logger = LoggerService.get_logger()
    handlers = [handler for handler in logger.handlers if isinstance(handler, RotatingFileHandler)]
    assert len(handlers) > 0
    handler = handlers[0]
    assert handler.maxBytes == 1_000_000
    assert handler.backupCount == 5

def test_logger_handlers_not_duplicated():
    logger = LoggerService.get_logger()
    initial_handlers_count = len(logger.handlers)
    logger2 = LoggerService.get_logger()
    assert logger2 is logger
    assert len(logger.handlers) == initial_handlers_count

def test_logger_can_log_messages(caplog):
    logger = LoggerService.get_logger()
    with caplog.at_level(logging.INFO):
        logger.info("Test info message")
        logger.warning("Test warning message")

    assert "Test info message" in caplog.text
    assert "Test warning message" in caplog.text
    