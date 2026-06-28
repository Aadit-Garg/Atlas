# Worker Lifecycle

Workers transition through specific lifecycle states managed by the Atlas Runtime.

1. **Discovered:** The `worker.yaml` manifest is found on disk.
2. **Registered:** The Worker's metadata (Roles, Imports, Exports) is loaded into the Runtime Registry.
3. **Initialized:** The Worker's code is loaded into memory (but no active logic runs).
4. **Started:** The Worker is instructed to boot up. It requests its imported Capabilities, establishes Sessions, and connects to the Data Plane.
5. **Running:** The normal operational state.
6. **Paused:** (Optional) The Worker is instructed to pause active operations (e.g., during snapshotting or migration).
7. **Stopped:** The Worker flushes state and disconnects from the Data Plane.
8. **Disposed:** The Worker is unloaded from memory.
