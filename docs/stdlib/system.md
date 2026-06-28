# System Workers

The **System** category abstracts host OS functionality, ensuring that Atlas applications can remain cross-platform (Windows, macOS, Linux) without scattering OS-specific `if/else` checks throughout the business logic.

---

## Process (`atlas.system.process`)

**Purpose:** Spawns and manages child processes safely.
**Implemented Model:** `ProcessModel`
**Roles:** `[system]`

### Public APIs
- `execute(command: str, args: list[str]) -> dict` (Returns stdout, stderr, and exit code).
- `spawn(command: str, args: list[str]) -> str` (Returns a Process ID for background tasks).
- `kill(pid: str) -> bool`

### Testing Strategy
The `ProcessModel` can be easily mocked using Solon to simulate shell commands without actually running them during CI/CD.

---

## Terminal (`atlas.system.terminal`)

**Purpose:** Advanced CLI interaction, including colors, tables, and progress bars.
**Implemented Model:** `TerminalModel`
**Roles:** `[system, ui]`

### Public APIs
- `print(text: str, color: str = None) -> None`
- `prompt(question: str) -> str`
- `table(headers: list[str], rows: list[list[str]]) -> None`

### Dependencies
Usually implemented under the hood using libraries like `rich` in Python, but abstracts that dependency away from the rest of the application.

---

## Clipboard (`atlas.system.clipboard`)

**Purpose:** Reads from and writes to the user's system clipboard.
**Implemented Model:** `ClipboardModel`
**Roles:** `[system]`

### Public APIs
- `copy(text: str) -> bool`
- `paste() -> str`

---

## Notifications (`atlas.system.notifications`)

**Purpose:** Triggers native OS desktop notifications.
**Implemented Model:** `NotificationModel`
**Roles:** `[system, ui]`

### Public APIs
- `notify(title: str, message: str, urgency: str = "normal") -> bool`

### Failure Modes
If the host OS does not support notifications (e.g., a headless Linux server), this worker should fail gracefully (returning `False` or doing nothing) rather than crashing the application.

---

## Other Proposed System Workers

- **Shell:** Evaluates raw shell scripts.
- **OS Information:** Retrieves platform details (CPU architecture, memory usage, OS version) for telemetry and diagnostic workers.
