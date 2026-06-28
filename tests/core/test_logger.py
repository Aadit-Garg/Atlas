import logging
from atlas.core.logger import AtlasLogger


def test_atlas_logger_init():
    logger = AtlasLogger(name="test_logger", level=logging.DEBUG)
    assert logger._logger.name == "test_logger"
    assert logger._logger.level == logging.DEBUG
    assert len(logger._logger.handlers) == 1


def test_atlas_logger_formatting(caplog):
    logger = AtlasLogger(name="test_logger")
    logger.set_level(logging.INFO)
    logger._logger.propagate = True
    
    with caplog.at_level(logging.INFO):
        logger.info("Test message", user="alice", action="login")
        
    assert "Test message | user=alice action=login" in caplog.text


def test_atlas_logger_child():
    parent = AtlasLogger(name="parent")
    child = parent.child("child")
    
    assert child._logger.name == "parent.child"
    assert child._logger.level == parent._logger.level
