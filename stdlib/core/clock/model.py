from abc import ABC, abstractmethod

class ClockModel(ABC):
    """
    Official Atlas Standard Model for Timekeeping.
    Defines the contract for any worker claiming the 'atlas.core.clock' capability.
    """
    @abstractmethod
    def now(self) -> str:
        """Returns the current UTC time in ISO 8601 format."""
        pass

    @abstractmethod
    def timestamp(self) -> float:
        """Returns the current unix timestamp."""
        pass

    @abstractmethod
    def sleep(self, seconds: float) -> None:
        """Sleeps the calling thread for the given number of seconds."""
        pass
