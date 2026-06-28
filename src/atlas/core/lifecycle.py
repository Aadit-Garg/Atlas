"""
Lifecycle Manager for Atlas Core.

Coordinates the state transitions for Workers.
"""
from enum import Enum
import asyncio

from atlas.core.protocols import LifecycleProtocol
from atlas.core.logger import LoggerProtocol
from atlas.core.errors import InvalidTransitionError, InitializationError


class LifecycleState(str, Enum):
    REGISTERED = "Registered"
    INITIALIZED = "Initialized"
    STARTED = "Started"
    RUNNING = "Running"
    PAUSED = "Paused"
    STOPPED = "Stopped"
    DISPOSED = "Disposed"
    ERROR = "Error"


class LifecycleManager:
    def __init__(self, logger: LoggerProtocol):
        self._logger = logger.child("lifecycle")
        self._workers: list[LifecycleProtocol] = []

    def manage(self, worker: LifecycleProtocol) -> None:
        if worker not in self._workers:
            self._workers.append(worker)

    async def initialize_all(self) -> None:
        self._logger.info("Initializing Workers...")
        tasks = []
        for worker in self._workers:
            if getattr(worker, "state", None) == LifecycleState.REGISTERED.value:
                tasks.append(self._safe_transition(worker, "initialize", LifecycleState.INITIALIZED))
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    raise InitializationError(
                        message="One or more workers failed to initialize.",
                        reason=str(result),
                        cause=result
                    )

    async def start_all(self) -> None:
        self._logger.info("Starting Workers...")
        tasks = []
        for worker in self._workers:
            if getattr(worker, "state", None) == LifecycleState.INITIALIZED.value:
                tasks.append(self._safe_transition(worker, "start", LifecycleState.STARTED))
                
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    raise InitializationError("One or more workers failed to start.", reason=str(result), cause=result)

    async def stop_all(self) -> None:
        self._logger.info("Stopping Workers...")
        tasks = []
        for worker in reversed(self._workers):
            state = getattr(worker, "state", None)
            if state in (LifecycleState.STARTED.value, LifecycleState.RUNNING.value, LifecycleState.PAUSED.value):
                tasks.append(self._safe_transition(worker, "stop", LifecycleState.STOPPED))
                
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
    async def dispose_all(self) -> None:
        self._logger.info("Disposing Workers...")
        tasks = []
        for worker in reversed(self._workers):
            tasks.append(self._safe_transition(worker, "dispose", LifecycleState.DISPOSED))
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        self._workers.clear()

    async def _safe_transition(self, worker: LifecycleProtocol, method_name: str, target_state: LifecycleState) -> None:
        worker_id = getattr(worker, "id", worker.__class__.__name__)
        try:
            method = getattr(worker, method_name)
            await method()
        except Exception as e:
            self._logger.error(f"Transition {method_name} failed for {worker_id}: {e}")
            raise InvalidTransitionError(
                message=f"Worker {worker_id} failed during {method_name}.",
                reason=str(e),
                cause=e
            ) from e
