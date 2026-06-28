import os
import yaml
from atlas.core.configuration import ConfigurationManager, deep_merge


def test_deep_merge():
    target = {"a": 1, "b": {"c": 2}}
    source = {"b": {"d": 3}, "e": 4, "a": None}
    
    result = deep_merge(target, source)
    assert result == {"b": {"c": 2, "d": 3}, "e": 4}
    assert "a" not in result


def test_parse_environment_variables(monkeypatch):
    monkeypatch.setenv("ATLAS_RUNTIME__LOG_LEVEL", "debug")
    monkeypatch.setenv("ATLAS_STORAGE__PROVIDER", "postgres")
    monkeypatch.setenv("ATLAS_SOME__NESTED__KEY", "42")
    
    config = ConfigurationManager()
    env_overrides = config._parse_environment_variables()
    
    assert env_overrides["runtime"]["log_level"] == "debug"
    assert env_overrides["storage"]["provider"] == "postgres"
    assert env_overrides["some"]["nested"]["key"] == 42


def test_config_load_and_get(tmp_path):
    config_file = tmp_path / "atlas.yaml"
    config_data = {
        "runtime": {"log_level": "info"}
    }
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
        
    config = ConfigurationManager()
    config.load(base_path=str(config_file))
    
    assert config.get("runtime.log_level") == "info"
    assert config.get("nonexistent", "default") == "default"
    assert config.has("runtime.log_level") is True
