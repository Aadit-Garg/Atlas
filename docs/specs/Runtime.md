# Runtime

The Atlas Runtime is the instantiated process of Atlas Core.

The Runtime intentionally remains very small. Its sole purpose is to manage the Global Registry, instantiate Room Stewards, and coordinate lifecycle changes.

## Execution Flow

1. **Boot:** The Runtime starts and populates the Global Registry via discovery.
2. **Resolution Check:** The Runtime verifies that all Worker dependencies (Capabilities) can be fulfilled.
3. **Room Creation:** When an orchestration Worker requests a collaboration, the Runtime spawns a **Room Steward** to manage that context.
4. **Binding:** The Room Steward reads the communication Headers and establishes Sessions between Workers inside the Room.
5. **Invocation:** Workers execute Invocations (the requests sent over Sessions).
6. **Shutdown:** The Runtime pauses Rooms, drains Invocations, and gracefully terminates.

## Failure Handling

If a critical Worker fails during execution:
1. Atlas instantly transitions affected Rooms into the `Frozen` state.
2. The freeze propagates through participating Rooms topologically.
3. Workers are allowed to finish active operations where possible.
4. Recovery procedures are triggered. Execution only resumes once recovery completes.

Room state transitions heavily prioritize graceful recovery over hard crashing.