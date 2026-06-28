import pytest
from stdlib.core.logger.worker import ConsoleLoggerWorker

def test_console_logger_implements_model():
    logger = ConsoleLoggerWorker()
    
    # Simple execution test to ensure no crashes
    logger.debug("Test debug")
    logger.info("Test info", context={"user": "miron"})
    logger.warn("Test warn")
    logger.error("Test error", exc_info="ValueError: test")
    
    # Check if handlers were bound correctly
    assert len(logger.logger.handlers) == 1
    assert logger.logger.level == 10 # logging.DEBUG
