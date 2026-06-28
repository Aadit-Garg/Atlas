import pytest
import asyncio
from atlas.core.session import SessionManager, Session
from atlas.core.registry import Registry
from atlas.core.logger import AtlasLogger
from atlas.core.errors import WorkerNotAvailableError


class DummyWorker:
    def __init__(self, wid):
        self.id = wid
        self.version = "1.0"
        
    async def bind_capability(self, capability_name: str, requesting_worker_id: str):
        return {"connection": "active"}


@pytest.mark.asyncio
async def test_session_establishment():
    logger = AtlasLogger()
    registry = Registry(logger)
    
    provider_worker = DummyWorker("worker.sqlite")
    registry.register_worker(provider_worker) # type: ignore
    
    session_manager = SessionManager(registry, logger)
    session_manager.register_export("capability.storage", "worker.sqlite")
    
    requesting_worker = DummyWorker("worker.journal")
    
    session = await session_manager.establish_session(requesting_worker, "capability.storage") # type: ignore
    
    assert session is not None
    assert session.source_worker_id == "worker.journal"
    assert session.target_worker_id == "worker.sqlite"
    assert session.binding == {"connection": "active"}


@pytest.mark.asyncio
async def test_session_worker_unavailable():
    logger = AtlasLogger()
    registry = Registry(logger)
    session_manager = SessionManager(registry, logger)
    
    requesting_worker = DummyWorker("worker.journal")
    
    with pytest.raises(WorkerNotAvailableError):
        await session_manager.establish_session(requesting_worker, "capability.not_found") # type: ignore
