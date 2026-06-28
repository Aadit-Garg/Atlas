from abc import ABC, abstractmethod
from typing import Optional, Any

class ConfigModel(ABC):
    """
    Official Atlas Standard Model for Configuration.
    Defines the contract for any worker claiming the 'atlas.core.config' capability.
    """
    @abstractmethod
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def has(self, key: str) -> bool:
        pass
