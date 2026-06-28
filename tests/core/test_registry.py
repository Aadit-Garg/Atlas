import pytest
from atlas.core.registry import Registry
from atlas.core.logger import AtlasLogger
from atlas.core.errors import DuplicateRegistrationError


class DummyManifest:
    roles = ["database", "storage"]


class DummyWorker:
    id = "dummy.worker"
    name = "Dummy"
    version = "1.0"
    state = "Registered"
    manifest = DummyManifest()


class DummyModel:
    name = "storage.sql"
    version = "1.0"


def test_registry_registration():
    registry = Registry(logger=AtlasLogger())
    worker = DummyWorker()
    model = DummyModel()
    
    registry.register_worker(worker) # type: ignore
    registry.register_model(model) # type: ignore
    
    assert registry.get_worker("dummy.worker") == worker
    assert registry.get_model("storage.sql", "1.0") == model
    
    # Test Roles Indexing
    workers_with_db = registry.get_workers_by_role("database")
    assert len(workers_with_db) == 1
    assert workers_with_db[0].id == "dummy.worker"


def test_registry_duplicate_error():
    registry = Registry(logger=AtlasLogger())
    worker = DummyWorker()
    
    registry.register_worker(worker) # type: ignore
    with pytest.raises(DuplicateRegistrationError):
        registry.register_worker(worker) # type: ignore
