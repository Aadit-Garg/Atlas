import os
import importlib.util
import sys
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .diagnostics import Result, LoadError, MissingSymbolError
from .manifest import WorkerManifest

# ---------------------------------------------------------
# Dynamic Loader Data Structures
# ---------------------------------------------------------

@dataclass
class WorkerInstance:
    """
    Represents an executable Worker loaded into memory.
    The `_executable_handle` is strictly owned by the Loader.
    """
    id: str
    manifest: WorkerManifest
    _executable_handle: Any  # Language-specific pointer/module

# ---------------------------------------------------------
# Language Strategies
# ---------------------------------------------------------

class LanguageLoaderStrategy(ABC):
    @abstractmethod
    def load(self, manifest: WorkerManifest, source_path: str) -> Result[Any, Exception]:
        pass

    @abstractmethod
    def unload(self, handle: Any) -> Result[None, Exception]:
        pass

    @abstractmethod
    def verify_entry_point(self, handle: Any) -> Result[None, Exception]:
        pass


class PythonLoaderStrategy(LanguageLoaderStrategy):
    """Dynamically loads Python Workers using importlib."""
    
    def load(self, manifest: WorkerManifest, source_path: str) -> Result[Any, Exception]:
        module_name = f"atlas.workers.{manifest.id.replace('.', '_')}"
        
        # Determine if it's a package or a single file
        init_file = os.path.join(source_path, "src", "__init__.py")
        py_file = os.path.join(source_path, "src", f"{manifest.name}.py")
        
        target_file = init_file if os.path.exists(init_file) else py_file
        
        if not os.path.exists(target_file):
            return Result.err(LoadError(f"Executable entry not found for Python worker", context={"path": target_file}))

        try:
            spec = importlib.util.spec_from_file_location(module_name, target_file)
            if spec is None or spec.loader is None:
                return Result.err(LoadError("Failed to create module spec"))
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            return Result.ok(module)
        except SyntaxError as e:
            return Result.err(LoadError(f"Syntax error in worker: {e}", context={"file": target_file}))
        except Exception as e:
            return Result.err(LoadError(f"Failed to load python module: {e}", context={"file": target_file}))

    def unload(self, handle: Any) -> Result[None, Exception]:
        """Soft unload for Python."""
        try:
            if hasattr(handle, "__name__") and handle.__name__ in sys.modules:
                del sys.modules[handle.__name__]
            return Result.ok(None)
        except Exception as e:
            return Result.err(LoadError(f"Failed to unload python module: {e}"))

    def verify_entry_point(self, handle: Any) -> Result[None, Exception]:
        """Verify the module exposes a Worker entry point."""
        if not hasattr(handle, "Worker"):
            return Result.err(MissingSymbolError("Python module is missing 'Worker' class export"))
        return Result.ok(None)


# ---------------------------------------------------------
# The Dynamic Loader
# ---------------------------------------------------------

class DynamicLoader:
    def __init__(self):
        self._strategies: Dict[str, LanguageLoaderStrategy] = {
            "python": PythonLoaderStrategy()
            # Future: "rust": RustLoaderStrategy()
        }
        self._loaded_workers: Dict[str, WorkerInstance] = {}

    def load_worker(self, manifest: WorkerManifest, source_path: str) -> Result[WorkerInstance, Exception]:
        strategy = self._strategies.get(manifest.language.lower())
        if not strategy:
            return Result.err(LoadError(f"Unsupported language strategy: {manifest.language}"))

        # Step 1: Load into memory
        load_res = strategy.load(manifest, source_path)
        if load_res.is_err():
            return Result.err(load_res.error)

        handle = load_res.unwrap()

        # Step 2: Verify Symbols
        verify_res = strategy.verify_entry_point(handle)
        if verify_res.is_err():
            strategy.unload(handle) # Clean up partial load
            return Result.err(verify_res.error)

        instance = WorkerInstance(
            id=manifest.id,
            manifest=manifest,
            _executable_handle=handle
        )
        
        self._loaded_workers[manifest.id] = instance
        return Result.ok(instance)

    def unload_worker(self, worker_id: str) -> Result[None, Exception]:
        instance = self._loaded_workers.get(worker_id)
        if not instance:
            return Result.err(LoadError(f"Worker {worker_id} is not loaded"))

        strategy = self._strategies.get(instance.manifest.language.lower())
        if not strategy:
            return Result.err(LoadError(f"Lost strategy for {worker_id}"))

        unload_res = strategy.unload(instance._executable_handle)
        if unload_res.is_err():
            return Result.err(unload_res.error)

        del self._loaded_workers[worker_id]
        return Result.ok(None)
