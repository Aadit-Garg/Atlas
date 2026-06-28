"""
Configuration Manager for Atlas Core.
"""
import os
import yaml
from typing import Any
from atlas.core.protocols import ConfigurationProtocol
from atlas.core.errors import ConfigValidationError


def deep_merge(target: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    for key, value in source.items():
        if value is None:
            if key in target:
                del target[key]
        elif isinstance(value, dict) and key in target and isinstance(target[key], dict):
            target[key] = deep_merge(target[key], value)
        else:
            target[key] = value
    return target


class ConfigurationManager:
    def __init__(self) -> None:
        self._config: dict[str, Any] = {}

    def load(self, base_path: str = "atlas.yaml", environment: str | None = None) -> None:
        if os.path.exists(base_path):
            with open(base_path, "r", encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f) or {}
                    self._config = deep_merge(self._config, data)
                except yaml.YAMLError as e:
                    raise ConfigValidationError(
                        message=f"Failed to parse config {base_path}", reason=str(e)
                    ) from e

        env = environment or self.get("atlas.environment") or os.environ.get("ATLAS_ENV")
        if env:
            env_path = base_path.replace(".yaml", f".{env}.yaml")
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    self._config = deep_merge(self._config, data)

        self._config = deep_merge(self._config, self._parse_environment_variables())

    def _parse_environment_variables(self) -> dict[str, Any]:
        overrides: dict[str, Any] = {}
        for key, value in os.environ.items():
            if key.startswith("ATLAS_") and key != "ATLAS_ENV":
                path_str = key[len("ATLAS_"):]
                parts = [p.lower() for p in path_str.split("__")]
                
                parsed_value: Any = value
                if value.lower() in ("true", "1", "yes"): parsed_value = True
                elif value.lower() in ("false", "0", "no"): parsed_value = False
                elif value.isdigit(): parsed_value = int(value)

                current = overrides
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = parsed_value
        return overrides

    def get(self, key: str, default: Any = None) -> Any:
        parts = key.split(".")
        current = self._config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current

    def get_section(self, section: str) -> dict[str, Any]:
        value = self.get(section)
        return value if isinstance(value, dict) else {}

    def has(self, key: str) -> bool:
        parts = key.split(".")
        current = self._config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        return True
