import os
from atlas.core.manifest import ManifestLoader
from atlas.core.loader import DynamicLoader
from atlas.core.diagnostics import LoadError

def test_valid_python_load():
    manifest_loader = ManifestLoader()
    worker_dir = os.path.join(os.path.dirname(__file__), "dummy_workers", "valid")
    path = os.path.join(worker_dir, "atlas.yaml")
    
    manifest = manifest_loader.load_file(path).unwrap()
    
    loader = DynamicLoader()
    res = loader.load_worker(manifest, worker_dir)
    assert res.is_ok()
    
    instance = res.unwrap()
    assert instance.id == "atlas.test.dummy"
    assert instance._executable_handle is not None
    assert hasattr(instance._executable_handle, "Worker")
    
    # Test Unload
    res = loader.unload_worker(instance.id)
    assert res.is_ok()

def test_unsupported_language():
    manifest_loader = ManifestLoader()
    worker_dir = os.path.join(os.path.dirname(__file__), "dummy_workers", "valid")
    path = os.path.join(worker_dir, "atlas.yaml")
    
    manifest = manifest_loader.load_file(path).unwrap()
    # Hack the language to unsupported
    object.__setattr__(manifest, "language", "rust")
    
    loader = DynamicLoader()
    res = loader.load_worker(manifest, worker_dir)
    assert res.is_err()
    assert isinstance(res.error, LoadError)
