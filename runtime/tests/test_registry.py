import os
from atlas.core.manifest import ManifestLoader
from atlas.core.loader import DynamicLoader
from atlas.core.registry import GlobalRegistry, HealthStatus
from atlas.core.diagnostics import IdCollisionError, LookupError

def test_registry_registration():
    # Setup
    manifest_loader = ManifestLoader()
    worker_dir = os.path.join(os.path.dirname(__file__), "dummy_workers", "valid")
    manifest = manifest_loader.load_file(os.path.join(worker_dir, "atlas.yaml")).unwrap()
    
    loader = DynamicLoader()
    instance = loader.load_worker(manifest, worker_dir).unwrap()
    
    # Registry Test
    registry = GlobalRegistry()
    res = registry.register_worker(instance)
    assert res.is_ok()
    
    # Test O(1) indices
    providers = registry.find_providers_for_capability("capability.storage.test")
    assert providers.is_ok()
    assert "atlas.test.dummy" in providers.unwrap()
    
    roles = registry.get_workers_by_role("test")
    assert len(roles) == 1
    assert roles[0].id == "atlas.test.dummy"
    
    # Duplicate Registration
    dup_res = registry.register_worker(instance)
    assert dup_res.is_err()
    assert isinstance(dup_res.error, IdCollisionError)
    
    # Deregister
    registry.deregister_worker(instance.id)
    assert registry.get_worker(instance.id) is None
    
    # Verify index pruned
    missing_providers = registry.find_providers_for_capability("capability.storage.test")
    assert missing_providers.is_err()
    assert isinstance(missing_providers.error, LookupError)
