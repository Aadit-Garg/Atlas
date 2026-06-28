# Phase 1.1: Global Registry Implementation Specification

The Global Registry is the central repository of macro-state runtime facts. It MUST NOT store business data. It provides O(1) lookups for routing and resolution.

---

## 1. Internal Storage & Indexing

The Registry maintains highly optimized, normalized tables (HashMaps).

```typescript
struct GlobalRegistryState {
    // Primary Key: Worker ID -> WorkerInstance
    workers: Map<String, WorkerInstance>;
    
    // Primary Key: Room ID -> Room Context (Milestone 1.4)
    rooms: Map<String, RoomInstance>;
    
    // Index: Capability Name -> List of providing Worker IDs
    capabilities_index: Map<String, List<String>>;
    
    // Index: Role Name -> List of Worker IDs
    roles_index: Map<String, List<String>>;
    
    // Health & Stats Tracking
    metrics: Map<String, WorkerMetrics>;
}
```

## 2. Lock Strategy & Concurrency

The Global Registry is the most highly contended resource in the platform. 

**Concurrency Model:**
- **Read-Write Lock (RwLock):** 
  - Multiple threads can read simultaneously (`get_worker`, `find_capabilities`).
  - Only one thread can write (`register_worker`, `deregister_worker`), which blocks reads temporarily.
- **Lock Granularity:** Fine-grained locks on specific tables rather than one massive lock on `GlobalRegistryState` to prevent a Room registration from blocking a Capability lookup.

## 3. Public API

```typescript
interface GlobalRegistry {
    // Mutators (Write Locks)
    register_worker(instance: WorkerInstance) -> Result<(), RegistryError>;
    deregister_worker(worker_id: String) -> Result<(), RegistryError>;
    
    // Accessors (Read Locks)
    get_worker(worker_id: String) -> Option<WorkerInstance>;
    get_workers_by_role(role: String) -> List<WorkerInstance>;
    find_providers_for_capability(capability: String) -> List<String>;
    
    // Health API
    update_worker_health(worker_id: String, status: HealthStatus);
}
```

## 4. Internal API & Synchronization

```typescript
// Synchronizes the capability index when a new worker is registered
_sync_capability_index(manifest: WorkerManifest);

// Prunes dead workers from indices
_clean_indices(worker_id: String);
```

## 5. Worker Registration Flow

When `register_worker` is called:
1. Acquire Write Lock on `workers`. Check for ID collision.
2. Insert into `workers`.
3. Acquire Write Lock on `capabilities_index`. Read exports from manifest and append Worker ID.
4. Acquire Write Lock on `roles_index`. Append Worker ID.
5. Initialize `WorkerMetrics` with `HealthStatus::Starting`.
6. Release locks. Broadcast `WorkerRegistered` internal event.

## 6. Performance & Scalability Considerations
- **O(1) Lookups:** By maintaining dedicated HashMaps for capabilities and roles, resolution avoids O(N) iteration over the worker list.
- **Cache Invalidation:** The Room Manager will cache resolution results locally. The Global Registry does not push invalidations; Room Stewards poll the Global Registry via quick checksums or version hashes to detect macro-state changes.
