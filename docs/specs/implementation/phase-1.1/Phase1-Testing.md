# Phase 1.1: Testing Strategy

This document defines the strict testing requirements for the Phase 1.1 components. Testing must guarantee that the core foundation will not collapse under failure or high concurrency.

---

## 1. Unit Tests (Isolation)

Every subsystem requires absolute isolation testing using mocked boundaries.

### Manifest Loader
- **Valid Schemas:** Parse full, valid `worker.yaml` files.
- **Missing Required Fields:** Ensure parsing fails gracefully if `id` or `language` is missing.
- **Type Mismatches:** Ensure parsing fails if `roles` is a string instead of a list.
- **SemVer Parsing:** Validate strict SemVer formatting on model versions.

### Dynamic Loader
- **Mock Strategy:** Test using dummy Python modules.
- **Missing Export:** Attempt to load a module that does not export `WorkerProtocol`. Should yield `MissingSymbolError`.
- **Syntax Error:** Attempt to load a structurally broken Python file. Should yield `LoadError` without crashing the test runner.

### Global Registry
- **Duplicate Registration:** Attempt to register two workers with the same ID.
- **Index Integrity:** Register a worker, verify it appears in `capabilities_index`, then deregister it and verify it is completely purged from all indices.

## 2. Integration Tests (Handoff)

- **End-to-End Load:** Pass a directory path to `ManifestLoader` -> pipe `WorkerManifest` to `DynamicLoader` -> pipe `WorkerInstance` to `GlobalRegistry.register_worker()`.
- Assert that the Worker is fully accessible and health status is tracked.

## 3. Concurrency Tests (Thread Safety)

The Global Registry must survive massive parallel access.

**Scenario: The Read/Write Flood**
- Spawn 100 threads.
- 10 threads continuously write (registering and deregistering dummy workers).
- 90 threads continuously read (querying capabilities).
- *Success Criteria:* No deadlocks, no race conditions, no `KeyError` during reads while writes are occurring. (Requires strict RwLock implementation).

## 4. Stress Tests & Benchmarks

**Benchmark Strategy:**
- **Registry Lookup Speed:** Measure latency of `find_providers_for_capability()` under a load of 10,000 registered workers. Must remain sub-millisecond (O(1) requirement).
- **Manifest Caching:** Measure parsing 1,000 files vs reading from cache.

## 5. Failure Injection (Chaos)

- **Permission Denial:** Restrict file read permissions on `worker.yaml` right before the Manifest Loader attempts to read it. Verify structured `IOError` propagates cleanly.
- **Mid-Load File Deletion:** Delete the executable file immediately after the Manifest Loader parses it, but before the Dynamic Loader runs. Verify `LoadError` occurs and the Registry state remains clean.
