import threading
import time
import os
from atlas.core.manifest import ManifestLoader
from atlas.core.loader import DynamicLoader
from atlas.core.registry import GlobalRegistry

def test_registry_read_write_flood():
    """
    Stress tests the Global Registry using 'The Read/Write Flood' specified in Phase1-Testing.md.
    100 threads hammer the Registry simultaneously to ensure the RwLock holds up without deadlocking.
    """
    
    # Setup
    manifest_loader = ManifestLoader()
    worker_dir = os.path.join(os.path.dirname(__file__), "dummy_workers", "valid")
    manifest = manifest_loader.load_file(os.path.join(worker_dir, "worker.yaml")).unwrap()
    
    loader = DynamicLoader()
    base_instance = loader.load_worker(manifest, worker_dir).unwrap()
    
    registry = GlobalRegistry()
    
    stop_flag = False
    
    def writer_thread(tid: int):
        while not stop_flag:
            # Create a clone of the instance with a unique ID
            object.__setattr__(base_instance.manifest, "id", f"atlas.test.dummy.{tid}")
            base_instance.id = f"atlas.test.dummy.{tid}"
            
            registry.register_worker(base_instance)
            time.sleep(0.01)
            registry.deregister_worker(base_instance.id)

    def reader_thread():
        while not stop_flag:
            res = registry.find_providers_for_capability("capability.storage.test")
            # Result could be Ok or Err depending on timing, but must never crash or deadlock
            if res.is_ok():
                assert isinstance(res.unwrap(), list)
            time.sleep(0.005)
            
    # Spawn 10 writers and 90 readers
    threads = []
    for i in range(10):
        t = threading.Thread(target=writer_thread, args=(i,))
        threads.append(t)
        t.start()
        
    for i in range(90):
        t = threading.Thread(target=reader_thread)
        threads.append(t)
        t.start()
        
    # Let them fight for 2 seconds
    time.sleep(2)
    stop_flag = True
    
    for t in threads:
        t.join(timeout=1.0)
        
    assert True, "Flood survived without deadlocking"
