# Storage Workers

The **Storage** category provides a unified, declarative interface for persisting data. By using the models in this category, applications can seamlessly switch between memory, local files, and remote databases without changing business logic.

---

## Storage Model (`atlas.storage.*`)

**Purpose:** The foundational contract for key-value and blob storage.
**Implemented Model:** `StorageModel`
**Roles:** `[database, storage]`

### The Contract (Public APIs)
Any worker implementing `StorageModel` must provide:
- `write(key: str, data: bytes) -> bool`
- `read(key: str) -> bytes` (Returns empty bytes or raises an error if not found, depending on strictness)
- `delete(key: str) -> bool`
- `exists(key: str) -> bool`
- `list(prefix: str = "") -> list[str]`

### Implementations

#### 1. Filesystem Storage (`atlas.storage.fs`)
Writes raw bytes to the host OS filesystem.
- **Dependencies:** `atlas.core.config` (to resolve `STORAGE_ROOT_PATH`).
- **Performance:** Bounded by OS disk I/O. Use for large blobs (images, documents).

#### 2. SQLite Storage (`atlas.storage.sqlite`)
Stores key-value pairs in a local relational database.
- **Dependencies:** `atlas.core.config` (to resolve `DB_PATH`).
- **Performance:** Excellent for concurrent reads. Writes are locked per the SQLite connection.

#### 3. Memory Storage (`atlas.storage.memory`)
Stores data in a volatile Python dictionary.
- **Lifecycle:** All data is lost when the Manager shuts down.
- **Performance:** Ultra-fast. Used for testing and ephemeral caching.

---

## Document Storage Model (`atlas.storage.document.*`)

**Purpose:** While `StorageModel` handles raw bytes, the Document model handles structured data (JSON/Dictionaries).
**Implemented Model:** `DocumentModel`
**Roles:** `[database]`

### The Contract (Public APIs)
- `insert(collection: str, doc_id: str, document: dict) -> bool`
- `get(collection: str, doc_id: str) -> dict`
- `query(collection: str, filters: dict) -> list[dict]`
- `delete(collection: str, doc_id: str) -> bool`

### Implementations

#### 1. JSON Storage (`atlas.storage.document.json`)
Saves collections as `.json` files on disk.
- **Failure Modes:** Susceptible to corruption if the process crashes mid-write. Should implement atomic writes (write to temp file, then rename).

#### 2. YAML / TOML Storage
Similar to JSON, but heavily used for user-editable configuration files.

---

## Cache (`atlas.storage.cache`)

**Purpose:** Provides fast, temporary storage with TTL (Time To Live) semantics.
**Implemented Model:** `CacheModel`
**Roles:** `[utility, cache]`

### Public APIs
- `set(key: str, value: bytes, ttl_seconds: int) -> bool`
- `get(key: str) -> bytes`
- `invalidate(key: str) -> None`
- `clear() -> None`

### Lifecycle
Can be backed by `atlas.storage.memory` or a dedicated external Redis worker (if provided by a third-party). The standard library implementation uses an in-memory dictionary with a background cleanup thread.

---

## Other Proposed Storage Workers

- **CSV:** Specialized worker for appending row-based data, highly useful for telemetry and data science applications.
- **Binary Storage:** Optimized for chunked streaming of large files (video/audio).
