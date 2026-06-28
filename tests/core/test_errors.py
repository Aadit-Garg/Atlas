import pytest
from atlas.core.errors import AtlasError, ConfigNotFoundError


def test_atlas_error_base():
    err = AtlasError(
        message="Test message",
        reason="Test reason",
        context={"key": "value"},
        resolution="Test resolution"
    )
    
    assert err.message == "Test message"
    assert err.reason == "Test reason"
    assert err.context == {"key": "value"}
    assert err.resolution == "Test resolution"


def test_error_hierarchy():
    err = ConfigNotFoundError(message="msg", reason="reason")
    assert isinstance(err, AtlasError)
