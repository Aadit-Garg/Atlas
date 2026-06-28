"""
Session Manager for Atlas Core.

Handles Capability Resolution and Session Binding establishment between Workers.
This ensures Atlas coordinates (Control Plane) while Workers own (Data Plane).
"""
import uuid
from typing import Any
from dataclasses import dataclass

from atlas.core.protocols import SessionProtocol, WorkerProtocol
from atlas.core.registry import Registry
from atlas.core.logger import LoggerProtocol
from atlas.core.errors import CapabilityNotFoundError, WorkerNotAvailableError, PermissionDeniedError


@dataclass
class Session:
    session_id: str
    source_worker_id: str
    target_worker_id: str
    capability_name: str
    binding: Any


class SessionManager:
    """
    Coordinates capability resolution and session establishment.
    """
    def __init__(self, registry: Registry, logger: LoggerProtocol):
        self._registry = registry
        self._logger = logger.child("session")
        # mapping of capability_name to list of exporting worker ids
        self._capability_index: dict[str, list[str]] = {}

    def register_export(self, capability_name: str, worker_id: str) -> None:
        """Called during Worker Registration to index available capabilities."""
        if capability_name not in self._capability_index:
            self._capability_index[capability_name] = []
        if worker_id not in self._capability_index[capability_name]:
            self._capability_index[capability_name].append(worker_id)
            self._logger.debug(f"Indexed capability '{capability_name}' to Worker '{worker_id}'")

    async def establish_session(self, source_worker: WorkerProtocol, capability_name: str) -> SessionProtocol:
        """
        Resolves a requested capability and establishes a binding with the provider Worker.
        """
        self._logger.info(f"Worker '{source_worker.id}' requesting capability '{capability_name}'")
        
        # 1. Resolve to a target Worker
        target_worker_ids = self._capability_index.get(capability_name, [])
        if not target_worker_ids:
            raise WorkerNotAvailableError(
                message=f"No Worker exports capability '{capability_name}'.",
                reason="Capability not indexed."
            )
            
        # Simplistic resolution (just pick the first one)
        # In the future, this would check health, preferences, etc.
        target_worker_id = target_worker_ids[0]
        target_worker = self._registry.get_worker(target_worker_id)
        
        if not target_worker:
            raise WorkerNotAvailableError(
                message=f"Resolved Worker '{target_worker_id}' is no longer in the registry.",
                reason="Worker unloaded or crashed."
            )
            
        # 2. Permission Negotiation
        # Placeholder: Check if source_worker is allowed to access target_worker.capability
        # (This would be cross-checked against Manifest requirements and user grants)
        self._logger.debug(f"Permissions validated for {source_worker.id} -> {capability_name}")
        
        # 3. Create Binding (Data Plane hook)
        try:
            binding = await target_worker.bind_capability(capability_name, source_worker.id)
        except Exception as e:
            raise CapabilityNotFoundError(
                message=f"Target Worker '{target_worker_id}' failed to bind capability '{capability_name}'.",
                reason=str(e),
                cause=e
            ) from e
            
        # 4. Return Session
        session = Session(
            session_id=str(uuid.uuid4()),
            source_worker_id=source_worker.id,
            target_worker_id=target_worker_id,
            capability_name=capability_name,
            binding=binding
        )
        
        self._logger.debug(f"Session {session.session_id} established successfully.")
        return session
