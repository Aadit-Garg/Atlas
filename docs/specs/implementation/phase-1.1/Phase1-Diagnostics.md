# Phase 1.1: Diagnostics & Error Handling Specification

The Atlas Runtime relies heavily on deterministic error propagation. Because it is language-neutral, failures in the Python/Rust boundary must be captured as structured, typed errors rather than generic stack traces.

---

## 1. Error Hierarchy

All errors derive from a base `AtlasError` structure.

```typescript
struct AtlasError {
    readonly code: String;           // e.g., "ERR_MANIFEST_INVALID"
    readonly severity: Severity;     // Fatal | Recoverable | Warning
    readonly message: String;
    readonly context: Map<String, String>; // e.g., {"worker_id": "sqlite", "file": "worker.yaml"}
}
```

### Manifest Loader Errors
- `ParseError`: Invalid YAML/JSON syntax. (Severity: Fatal to Worker)
- `ValidationError`: Schema mismatch. (Severity: Fatal to Worker)
- `ResolutionError`: Missing base manifest for inheritance. (Severity: Fatal to Worker)

### Dynamic Loader Errors
- `LoadError`: OS-level failure (File not found, permission denied). (Severity: Fatal to Worker)
- `MissingSymbolError`: Executable lacks the `WorkerProtocol` interface. (Severity: Fatal to Worker)

### Registry Errors
- `IdCollisionError`: Attempting to register an already existing Worker ID. (Severity: Recoverable - Reject registration).
- `LookupError`: Capability not found. (Severity: Recoverable - Return empty list).

## 2. Error Propagation & Boundaries

The Runtime absolutely **must not crash** because a single Worker failed to load. 

**Propagation Rule:**
- Functions internal to a subsystem use native language exceptions or Result types (e.g., Rust `Result`, Python `try/except`).
- The boundary of every subsystem (its Public API) MUST return a structured `Result<T, AtlasError>`. 

## 3. Logging & Telemetry

Atlas uses a structured event log rather than text-based `print()` statements.

```typescript
enum EventType {
    Boot,
    WorkerDiscovered,
    WorkerLoaded,
    RegistrationFailed,
}

struct TelemetryEvent {
    timestamp: u64;
    event_type: EventType;
    latency_ms: u32;         // Optional, used for load time tracking
    context: String;
}
```

**Key Telemetry Points for Phase 1.1:**
1. **Load Latency:** The Dynamic Loader must measure the time elapsed from invoking the OS loader to returning the `WorkerInstance`.
2. **Registry Size:** Emit telemetry every time the Global Registry crosses a threshold (e.g., 100, 1000 workers) to track memory footprint.

## 4. Recovery Strategies
If the Dynamic Loader encounters a syntax error in Python, the recovery hook MUST log the structured error, discard the `ExecutableHandle`, and immediately yield execution back to the Global orchestrator. Atlas will skip the Worker and continue booting remaining components.
