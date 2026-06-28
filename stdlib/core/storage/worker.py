import os
from typing import Optional, Union

from .model import StorageModel

class LocalDiskStorageWorker(StorageModel):
    """
    Reference Implementation of the StorageModel.
    Provides simple local disk key-value storage.
    """
    def __init__(self, base_dir: str = ".atlas/storage"):
        self.base_dir = os.path.abspath(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)

    def _get_path(self, key: str) -> str:
        # Prevent directory traversal
        safe_key = key.replace("..", "").lstrip("/")
        return os.path.join(self.base_dir, safe_key)

    def write(self, key: str, data: Union[str, bytes]) -> None:
        path = self._get_path(key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        mode = "wb" if isinstance(data, bytes) else "w"
        with open(path, mode) as f:
            f.write(data)

    def read(self, key: str) -> Optional[bytes]:
        path = self._get_path(key)
        if not os.path.exists(path):
            return None
            
        with open(path, "rb") as f:
            return f.read()

    def delete(self, key: str) -> bool:
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def exists(self, key: str) -> bool:
        return os.path.exists(self._get_path(key))
