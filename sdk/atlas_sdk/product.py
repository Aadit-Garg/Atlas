"""
Atlas SDK — Product Builder
============================

The ProductBuilder provides a declarative way to compose multiple
Workers into a complete Atlas Product (application).

Usage:
    from atlas_sdk import ProductBuilder

    product = (
        ProductBuilder("my_notes_app")
        .add_worker("atlas.core.logger")
        .add_worker("atlas.core.storage")
        .add_worker("my.notes.worker")
        .set_entry_point("my.notes.worker")
        .configure("STORAGE_PATH", "/data/notes")
        .build()
    )
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import yaml


@dataclass
class WorkerRef:
    """A reference to a Worker used in a Product."""
    worker_id: str
    config_overrides: Dict[str, Any] = field(default_factory=dict)
    is_entry_point: bool = False


@dataclass
class ProductManifest:
    """The complete manifest for an Atlas Product."""
    name: str
    version: str
    description: str
    workers: List[WorkerRef]
    config: Dict[str, Any]
    entry_point: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product": {
                "name": self.name,
                "version": self.version,
                "description": self.description,
            },
            "workers": [
                {
                    "id": w.worker_id,
                    "entry_point": w.is_entry_point,
                    **({"config": w.config_overrides} if w.config_overrides else {}),
                }
                for w in self.workers
            ],
            "config": self.config,
        }

    def write(self, path: str = "product.yaml") -> str:
        with open(path, "w") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)
        return path


class ProductBuilder:
    """
    Declaratively compose Workers into a complete Atlas Product.

    This is the canonical way to build Atlas applications.
    The builder pattern eliminates boilerplate and ensures
    every Product follows Atlas conventions.
    """

    def __init__(self, name: str, version: str = "1.0.0", description: str = ""):
        self._name = name
        self._version = version
        self._description = description
        self._workers: List[WorkerRef] = []
        self._config: Dict[str, Any] = {}
        self._entry_point: Optional[str] = None

    def add_worker(self, worker_id: str, **config_overrides) -> "ProductBuilder":
        """
        Adds a Worker to the Product by its capability ID.

        Example::

            builder.add_worker("atlas.core.logger")
            builder.add_worker("my.db.worker", DATABASE_URL="sqlite:///data.db")
        """
        self._workers.append(WorkerRef(
            worker_id=worker_id,
            config_overrides=config_overrides,
        ))
        return self

    def set_entry_point(self, worker_id: str) -> "ProductBuilder":
        """
        Sets the primary entry point Worker for this Product.
        This is the Worker that gets invoked first when the Product starts.
        """
        self._entry_point = worker_id
        for w in self._workers:
            w.is_entry_point = (w.worker_id == worker_id)
        return self

    def configure(self, key: str, value: Any) -> "ProductBuilder":
        """
        Sets a global configuration value for the Product.
        Workers can read these via the ConfigModel.
        """
        self._config[key] = value
        return self

    def build(self) -> ProductManifest:
        """
        Builds and returns the final ProductManifest.
        Validates that at least one worker exists.
        """
        if not self._workers:
            raise ValueError("A Product must contain at least one Worker. Did you forget .add_worker()?")

        return ProductManifest(
            name=self._name,
            version=self._version,
            description=self._description,
            workers=self._workers,
            config=self._config,
            entry_point=self._entry_point,
        )
