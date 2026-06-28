# Runtime

The Atlas Runtime is the instantiated process of Atlas Core.

## Execution Flow

1. **Boot:** The Runtime starts and loads configuration.
2. **Discovery:** The Runtime parses the file system (or registry) to find installed `worker.yaml` manifests.
3. **Registration:** The Runtime populates its internal Registry with metadata about discovered Workers, Roles, Imports, and Exports.
4. **Resolution Check:** Before executing any Worker, the Runtime verifies that all strict `imports` (required Capabilities) can be resolved to registered `exports`.
5. **Startup:** The Runtime invokes the startup lifecycle hooks on the Workers (respecting topological dependencies).
6. **Binding:** When a Worker requests its imported Capability at runtime, the Runtime establishes a Session, negotiates permissions, and hands the binding reference to the Worker.
7. **Direct Communication:** The Workers use the binding to communicate directly. The Runtime steps out of the way.
8. **Shutdown:** The Runtime pauses Workers, flushes states (if instructed by the Worker), and gracefully terminates.

## Sessions

A **Session** is the runtime artifact of a resolved Capability. It represents an active, permission-validated connection between two Workers. Once a Session is returned by the Runtime, the Data Plane is open between the two Workers.