import os
from typing import Optional, Any, Dict

from models.core.config_model import ConfigModel

class EnvConfigWorker(ConfigModel):
    """
    Reference Implementation of the ConfigModel.
    Provides standard environment variable and local override configuration.
    """
    def __init__(self):
        self._local_overrides: Dict[str, Any] = {}

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        if key in self._local_overrides:
            return self._local_overrides[key]
        return os.environ.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._local_overrides[key] = value

    def has(self, key: str) -> bool:
        return key in self._local_overrides or key in os.environ
