import sys
import os
import importlib.util
import yaml

def main(args=None):
    if args is None:
        args = sys.argv[1:]
        
    if not args:
        print("❌ Error: Missing command for Atlas Suite.")
        print("Usage: atlas suite run <manager>")
        sys.exit(1)
        
    command = args[0]
    
    if command == "run":
        if len(args) < 2:
            print("❌ Error: Missing manager name to run.")
            print("Usage: atlas suite run <manager>")
            sys.exit(1)
            
        manager = args[1]
        
        # Read suite metadata to validate the manager exists in the suite
        suite_dir = os.path.dirname(os.path.abspath(__file__))
        suite_yaml = os.path.join(suite_dir, "atlas.yaml")
        
        try:
            with open(suite_yaml, "r", encoding="utf-8") as f:
                suite_data = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Error: Could not read suite metadata: {e}")
            sys.exit(1)
            
        allowed_managers = suite_data.get("managers", [])
        if manager not in allowed_managers:
            print(f"❌ Error: Manager '{manager}' is not registered in the suite metadata.")
            sys.exit(1)
        
        # Resolve the manager directory within the suite folder
        manager_dir = os.path.join(suite_dir, manager)
        
        if not os.path.isdir(manager_dir):
            print(f"❌ Error: Manager '{manager}' not found in Atlas Suite.")
            sys.exit(1)
            
        main_script = os.path.join(manager_dir, "main.py")
        if not os.path.isfile(main_script):
            print(f"❌ Error: Manager '{manager}' missing main.py entry point.")
            sys.exit(1)
            
        # Dynamically load and execute the manager's main.py
        module_name = f"atlas.suite.{manager}.main"
        spec = importlib.util.spec_from_file_location(module_name, main_script)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            try:
                spec.loader.exec_module(module)
                if hasattr(module, "main"):
                    # Pass the rest of the arguments to the manager
                    module.main(args[2:])
                else:
                    print(f"❌ Error: Manager '{manager}' missing main() function in {main_script}")
                    sys.exit(1)
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error executing Suite manager '{manager}': {e}")
                import traceback
                traceback.print_exc()
                sys.exit(1)
        else:
            print(f"❌ Error: Failed to load module {main_script}")
            sys.exit(1)
    else:
        print(f"❌ Error: Unknown suite command '{command}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
