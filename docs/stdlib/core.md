# Core Workers

The **Core** category contains the essential utilities for application lifecycle, state management, and foundational primitives. These are the workers that almost every Atlas application will need.

---

## Logger (`atlas.core.logger`)

**Purpose:** Provides a centralized, thread-safe, and context-aware logging mechanism for the entire application.
**Implemented Model:** `LoggerModel`
**Roles:** `[utility, observer]`

### Public APIs
- `info(message: str, context: dict = None) -> None`
- `warn(message: str, context: dict = None) -> None`
- `error(message: str, exc_info: str = None, context: dict = None) -> None`
- `debug(message: str, context: dict = None) -> None`

### Dependencies
None.

### Lifecycle & Configuration
- Executed as a `singleton`.
- **Config:** `LOG_LEVEL` (default: `INFO`).

### Failure Modes & Performance
- Should never throw exceptions that crash the caller. If logging fails (e.g., out of disk space for a file logger), it should degrade gracefully.
- Operations must be non-blocking.

---

## Configuration (`atlas.core.config`)

**Purpose:** Manages the injection, resolution, and caching of application configuration variables from multiple sources (ManagerBuilder, Environment, `.env`).
**Implemented Model:** `ConfigModel`
**Roles:** `[utility, provider]`

### Public APIs
- `get(key: str, default: str = None) -> str`
- `has(key: str) -> bool`
- `keys() -> list[str]`

### Dependencies
- May rely on `atlas.core.logger` for debugging config resolution.

### Lifecycle & Configuration
- Executed as a `singleton`.
- Fully loaded during `on_start()`. Read-only after boot to guarantee deterministic execution.

---

## Clock (`atlas.core.clock`)

**Purpose:** Provides deterministic time primitives. Essential for testing time-dependent logic without relying on the host OS clock directly.
**Implemented Model:** `ClockModel`
**Roles:** `[utility]`

### Public APIs
- `now() -> str` (ISO 8601 formatted UTC string)
- `timestamp() -> float` (Unix epoch time)
- `sleep(seconds: float) -> None`

### Dependencies
None.

### Testing Strategy
In test environments, the `ClockModel` is usually mocked by Solon to allow time-travel debugging and instantaneous sleeps.

---

## UUID (`atlas.core.uuid`)

**Purpose:** Generates unique identifiers for entities, messages, or sessions.
**Implemented Model:** `UUIDModel`
**Roles:** `[utility]`

### Public APIs
- `v4() -> str` (Standard random UUID)
- `v7() -> str` (Time-ordered UUID)

### Performance Considerations
Must be highly optimized as it is heavily used by the runtime for Message tracking.

---

## Scheduler (`atlas.core.scheduler`)

**Purpose:** Executes invocations on a recurring basis or after a delay.
**Implemented Model:** `SchedulerModel`
**Roles:** `[orchestrator]`

### Public APIs
- `schedule(cron: str, capability: str, payload: dict) -> str` (Returns Job ID)
- `delay(seconds: float, capability: str, payload: dict) -> str`
- `cancel(job_id: str) -> bool`

### Dependencies
- Requires `atlas.core.clock`.

### Failure Modes
If a scheduled invocation fails, the Scheduler logs the error via `LoggerModel` but continues running subsequent jobs.

---

## Other Proposed Core Workers

- **Environment:** Reads OS-level environment variables strictly.
- **Settings:** Persistent user preferences (usually wraps a Storage worker).
- **Registry Client:** Exposes read-only access to the Room Registry for telemetry observers.
- **Resource Loader:** Manages static assets bundled within `.atlas` packages.
- **Timer:** Measures execution durations for profiling.
- **Random:** Provides deterministic (seedable) random number generation for simulations and games.
