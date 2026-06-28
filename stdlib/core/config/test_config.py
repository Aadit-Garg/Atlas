import pytest
import os
from stdlib.core.config.worker import EnvConfigWorker

def test_env_config_implements_model():
    config = EnvConfigWorker()
    
    # Test local override
    config.set("ATLAS_TEST_KEY", "value123")
    assert config.get("ATLAS_TEST_KEY") == "value123"
    assert config.has("ATLAS_TEST_KEY") is True
    
    # Test env fallback
    os.environ["ATLAS_ENV_KEY"] = "env_value"
    assert config.get("ATLAS_ENV_KEY") == "env_value"
    assert config.has("ATLAS_ENV_KEY") is True
    
    # Test default
    assert config.get("MISSING_KEY", "default") == "default"
    assert config.has("MISSING_KEY") is False
