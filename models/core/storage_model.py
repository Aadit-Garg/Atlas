from abc import ABC, abstractmethod
from typing import Optional, Union

class StorageModel(ABC):
    """
    Official Atlas Standard Model for Key-Value / Blob Storage.
    Defines the contract for any worker claiming the 'atlas.core.storage' capability.
    """
    @abstractmethod
    def write(self, key: str, data: Union[str, bytes]) -> None:
        pass

    @abstractmethod
    def read(self, key: str) -> Optional[bytes]:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass
