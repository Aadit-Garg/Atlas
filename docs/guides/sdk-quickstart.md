# SDK Quickstart

> Get from zero to a running Atlas Worker in under 5 minutes.

---

## Prerequisites

- Python 3.13+
- Atlas CLI installed (`pip install -e .` from the Atlas repository root)

Verify your setup:

```bash
atlas doctor
```

---

## Step 1: Scaffold a Worker

```bash
atlas new
```

The interactive wizard will ask you:

1. **Type**: Select `worker`
2. **Name**: Enter `my_greeter`
3. **Namespace**: Enter `atlas` (or your own)
4. **Version**: Press Enter for `1.0.0`
5. **Description**: Enter `A simple greeter`
6. **Language**: Select `python`
7. **Confirm**: Press Enter to generate

This creates the following project:

```text
my_greeter/
├── atlas.yaml          # Worker manifest
├── worker.py           # Implementation
├── test_my_greeter.py  # Tests
└── README.md           # Documentation
```

---

## Step 2: Understand the Generated Code

### `worker.py`

```python
from atlas_sdk import WorkerBase, capability, on_invocation


class MyGreeterWorker(WorkerBase):
    _worker_id = "atlas.my_greeter"
    _worker_name = "MyGreeterWorker"
    _worker_version = "1.0.0"
    _worker_roles = ["worker"]

    def on_init(self):
        """Called after construction. Set up your state here."""
        pass

    def on_start(self):
        """Called when the runtime starts this worker."""
        pass

    def on_stop(self):
        """Called on shutdown. Clean up resources here."""
        pass

    @capability("atlas.my_greeter.hello", version="1.0.0")
    @on_invocation("hello")
    def hello(self, name: str = "World") -> str:
        """A simple hello capability. Replace me with real logic!"""
        return f"Hello, {name}! From MyGreeterWorker."
```

**Key concepts:**
- `WorkerBase` — The base class every Worker extends.
- `@capability(...)` — Exports a method so other Workers can discover and use it.
- `@on_invocation(...)` — Registers a method as a handler for incoming invocation requests.
- `on_init()` / `on_start()` / `on_stop()` — Lifecycle hooks called by the Runtime.

### `atlas.yaml`

The manifest declares your Worker's identity and capabilities to the Runtime:

```yaml
kind: worker
id: atlas.my_greeter
name: MyGreeterWorker
version: 1.0.0
language: python
roles: [worker]

exports:
  - capability: atlas.my_greeter
    version: 1.0.0
```

---

## Step 3: Add Real Logic

Let's make the greeter actually do something:

```python
from atlas_sdk import WorkerBase, capability, on_invocation


class MyGreeterWorker(WorkerBase):
    _worker_id = "atlas.my_greeter"
    _worker_name = "MyGreeterWorker"
    _worker_version = "1.0.0"
    _worker_roles = ["worker"]

    def on_init(self):
        self.greetings_sent = 0

    @capability("atlas.my_greeter.hello", version="1.0.0")
    @on_invocation("hello")
    def hello(self, name: str = "World") -> str:
        self.greetings_sent += 1
        return f"Hello, {name}! (Greeting #{self.greetings_sent})"

    @capability("atlas.my_greeter.stats", version="1.0.0")
    @on_invocation("stats")
    def stats(self) -> dict:
        return {"total_greetings": self.greetings_sent}
```

Update `atlas.yaml` to export the new capability:

```yaml
exports:
  - capability: atlas.my_greeter.hello
    version: 1.0.0
  - capability: atlas.my_greeter.stats
    version: 1.0.0
```

---

## Step 4: Test

```python
# test_my_greeter.py
from atlas_sdk.testing import MockRuntime, assert_capability_exported
from worker import MyGreeterWorker


def test_exports():
    worker = MyGreeterWorker()
    assert_capability_exported(worker, "atlas.my_greeter.hello")
    assert_capability_exported(worker, "atlas.my_greeter.stats")


def test_greeting():
    runtime = MockRuntime()
    runtime.register(MyGreeterWorker, "atlas.my_greeter")
    result = runtime.invoke("atlas.my_greeter", "hello", {"name": "Atlas"})
    assert "Hello, Atlas!" in result


def test_stats():
    runtime = MockRuntime()
    runtime.register(MyGreeterWorker, "atlas.my_greeter")
    runtime.invoke("atlas.my_greeter", "hello", {"name": "Test"})
    runtime.invoke("atlas.my_greeter", "hello", {"name": "Test"})
    stats = runtime.invoke("atlas.my_greeter", "stats")
    assert stats["total_greetings"] == 2
```

Run:

```bash
atlas test
```

---

## Step 5: Run

```bash
atlas run
```

This reads `atlas.yaml` from the current directory and boots the Atlas Runtime with your Worker loaded.

---

## What's Next?

| Guide | Description |
|---|---|
| [Building Workers](building-workers.md) | Deep dive into every file, decorator, lifecycle hook, and execution policy. |
| [Building Models](building-models.md) | Create abstract contracts that define capability interfaces. |
| [Building Adapters](building-adapters.md) | Build stateless format translation workers. |
| [Building Managers](building-managers.md) | Compose multiple Workers into a complete application. |
| [SDK Primitives](sdk-primitives.md) | Complete API reference for all SDK classes and functions. |
| [CLI Reference](cli-reference.md) | All available `atlas` commands and options. |
