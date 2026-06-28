from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class LoggerModel(ABC):
    """
    Official Atlas Standard Model for Logging.
    Defines the contract for any worker claiming the 'atlas.core.logger' capability.
    """
    @abstractmethod
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        pass

    @abstractmethod
    def info(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        pass

    @abstractmethod
    def warn(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        pass

    @abstractmethod
    def error(self, message: str, exc_info: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> None:
        pass
