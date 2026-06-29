import sys
import os
import yaml
from runtime.atlas.core.runtime import AtlasRuntime, RuntimeConfig
from rich.console import Console

console = Console()

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    # Boot the runtime
    config = RuntimeConfig(max_rooms=10, max_room_depth=1)
    runtime = AtlasRuntime(config)
    runtime.boot()
    
    manager_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(manager_dir, "atlas.yaml")

    try:
        # Load the manager's workers
        with open(manifest_path, "r") as f:
            manifest = yaml.safe_load(f)
            
        worker_manager = runtime.get_worker_manager()
        from runtime.atlas.core.manifest import ManifestLoader
        manifest_loader = ManifestLoader()
        
        for worker_req in manifest.get("workers", []):
            worker_id = worker_req.get("id")
            
            # Use Discovery Engine to find the worker
            from atlas_sdk.discovery import DiscoveryEngine
            atlas_root = os.path.dirname(os.path.dirname(os.path.dirname(manager_dir)))
            engine = DiscoveryEngine(atlas_root)
            worker_info = engine.find_worker(worker_id)
            
            if worker_info:
                load_res = manifest_loader.load_file(worker_info["manifest_path"])
                if load_res.is_err():
                    console.print(f"[bold red]❌ Failed to parse manifest for {worker_id}:[/bold red] {load_res.error}")
                    sys.exit(1)
                    
                manifest_obj = load_res.unwrap()
                res = worker_manager.request_worker(manifest_obj, worker_info["path"])
                if res.is_err():
                    console.print(f"[bold red]❌ Failed to load worker {worker_id}:[/bold red] {res.error}")
                    sys.exit(1)
            else:
                console.print(f"[bold red]❌ Could not discover worker:[/bold red] {worker_id}")
                sys.exit(1)

        # Retrieve the CLI worker from singletons
        # Since policy is singleton, it's stored by worker_id in the registry/manager
        cli_managed = None
        worker_manager._table_lock.acquire_read()
        try:
            cli_managed = worker_manager._singletons.get("atlas.studio.cli")
        finally:
            worker_manager._table_lock.release_read()
            
        if not cli_managed or not cli_managed.worker_instance:
            console.print("[bold red]❌ CLI Worker not found in runtime.[/bold red]")
            sys.exit(1)

        # Invoke the capability handler on the worker instance
        res = cli_managed.worker_instance._executable_handle.on_invoke("studio.cli.execute", {"args": args})
        if res.get("status") == "error":
            console.print(f"[bold red]❌ Studio CLI Error:[/bold red] {res.get('message')}")
            sys.exit(1)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        console.print(f"[bold red]❌ Fatal Error in Studio:[/bold red] {e}")
        from rich.traceback import install
        install(show_locals=False)
        raise
    finally:
        runtime.shutdown()

if __name__ == "__main__":
    main()
