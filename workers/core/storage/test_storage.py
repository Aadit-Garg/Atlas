import pytest
import os
import tempfile
from workers.core.storage.worker import LocalDiskStorageWorker

def test_local_disk_storage_implements_model():
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = LocalDiskStorageWorker(base_dir=temp_dir)
        
        # Test basic write/read (string)
        storage.write("user/profile.json", '{"name": "miron"}')
        assert storage.exists("user/profile.json") is True
        assert storage.read("user/profile.json") == b'{"name": "miron"}'
        
        # Test binary
        storage.write("data/blob.bin", b'\x00\x01\x02')
        assert storage.read("data/blob.bin") == b'\x00\x01\x02'
        
        # Test delete
        storage.delete("user/profile.json")
        assert storage.exists("user/profile.json") is False
        assert storage.read("user/profile.json") is None
        
        # Test traversal protection
        storage.write("../hack.txt", "hack")
        assert os.path.exists(os.path.join(temp_dir, "hack.txt")) is True
        assert os.path.exists(os.path.join(temp_dir, "..", "hack.txt")) is False
