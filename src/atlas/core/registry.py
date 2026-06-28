"""
Registry for Atlas Core (Worker Architecture).

Holds the discovered Workers and Models. Provides metadata lookup.
"""
from typing import Any

from atlas.core.protocols import RegistryProtocol, WorkerProtocol, ModelProtocol
from atlas.core.errors import DuplicateRegistrationError
from atlas.core.logger import LoggerProtocol


class Registry:
    """
    Central metadata registry for Atlas.
    """
    def __init__(self, logger: LoggerProtocol):
        self._logger = logger.child("registry")
        self._workers: dict[str, WorkerProtocol] = {}
        self._models: dict[str, ModelProtocol] = {}
        # Stores role -> list of worker IDs
        self._roles_index: dict[str, set[str]] = {}

    def register_worker(self, worker: WorkerProtocol) -> None:
        if worker.id in self._workers:
            raise DuplicateRegistrationError(
                message=f"Worker '{worker.id}' is already registered.",
                reason="Duplicate worker ID."
            )
        self._workers[worker.id] = worker
        
        # Index by roles if available
        if hasattr(worker, "manifest") and hasattr(worker.manifest, "roles"):
            for role in worker.manifest.roles:
                if role not in self._roles_index:
                    self._roles_index[role] = set()
                self._roles_index[role].add(worker.id)
                
        self._logger.debug(f"Registered Worker: {worker.id} (v{worker.version})")

    def register_model(self, model: ModelProtocol) -> None:
        model_id = f"{model.name}@{model.version}"
        if model_id in self._models:
            self._logger.warning(f"Model '{model_id}' is already registered. Overwriting.")
            
        self._models[model_id] = model
        self._logger.debug(f"Registered Model: {model_id}")

    def get_worker(self, worker_id: str) -> WorkerProtocol | None:
        return self._workers.get(worker_id)

    def get_model(self, model_name: str, version: str) -> ModelProtocol | None:
        return self._models.get(f"{model_name}@{version}")

    def get_workers_by_role(self, role: str) -> list[WorkerProtocol]:
        worker_ids = self._roles_index.get(role, set())
        return [self._workers[wid] for wid in worker_ids if wid in self._workers]
