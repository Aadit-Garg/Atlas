# Atlas Standard Library v1 (stdlib)

The **Atlas Standard Library** is the official collection of reusable Workers that form the foundation of the Atlas ecosystem. 

Because Atlas separates execution (Workers) from composition (Managers), this Standard Library is the vocabulary you use to build robust applications. The Library is purposefully small, cohesive, and language-agnostic. 

Whether you are using Studio, Miron, Solon, or building a bespoke application, these Workers are the foundational building blocks you will compose.

---

## Philosophy

- **Capabilities over Technologies:** We design the Standard Library around *what* it does, not *how* it does it. You request a `StorageModel`, not an `SQLiteWorker`.
- **Modularity:** Every Worker does exactly one thing well.
- **Models First:** The Standard Library provides declarative Models. Concrete Workers implement these Models. You should always program against the Model.
- **Language-Agnostic:** While the reference implementations are written in Python, the capabilities are universally accessible via Atlas Headers.

---

## The Dependency Philosophy

In traditional architectures, if your component needs to save data, you might import an SQLite library:

```text
MyComponent -> SQLite Library
```

In Atlas, this direct dependency is prohibited. Instead, the dependency flow is inverted through the Model system:

```text
MyWorker -> Storage Model
SQLiteWorker -> Storage Model
```

When you build a Manager, you compose your application by declaring that your Worker requires the `StorageModel`, and you provide the `SQLiteWorker` to fulfill it. This makes your logic instantly compatible with JSON storage, AWS S3, or In-Memory storage without changing a single line of your Worker's code.

---

## Catalog Overview

The Atlas Standard Library is organized into the following capability categories:

### 1. [Core](core.md)
The essential primitives for application lifecycle and foundational utilities.
- **Includes:** Logger, Configuration, Environment, Settings, Registry Client, Resource Loader, Timer, Scheduler, Clock, Random, UUID.

### 2. [Storage](storage.md)
Workers for data persistence, serialization, and caching.
- **Includes:** Filesystem, SQLite, JSON, YAML, TOML, CSV, Binary Storage, Cache.

### 3. [Networking](networking.md)
Workers for external communication and internet protocols.
- **Includes:** HTTP Client, HTTP Server, WebSocket, TCP, UDP, MQTT, DNS.

### 4. [System](system.md)
Workers for interacting with the host operating system.
- **Includes:** Process, Terminal, Clipboard, Notifications, Shell, OS Information.

### 5. [UI & Media](ui-media.md)
Workers for graphical interfaces and media manipulation (Optional/Extensions).
- **UI:** Window, Theme, Workspace, File Picker, Dialogs.
- **Media:** Image, Audio, Video, Camera, Microphone.

### 6. [AI & Hardware](ai-hardware.md)
Workers for machine learning capabilities and physical hardware interfacing.
- **AI:** Embedding, Inference, Tokenizer, Prompt, Vector Store.
- **Hardware:** GPIO, Serial, I2C, SPI, CAN, Motor, Camera, IMU, GPS, Bluetooth, Wi-Fi.

---

## SDK Integration

Every worker defined in this catalog can be scaffolded automatically using the Atlas CLI:

```bash
atlas new worker my_worker
```

When you build a project, you can easily pull any of these standard capabilities into your Manager:

```python
# main.py
from atlas_sdk import ManagerBuilder

def build():
    return (
        ManagerBuilder("MyApp", "1.0.0")
        .add_worker("atlas.core.logger")
        .add_worker("atlas.core.config")
        .add_worker("atlas.storage.sqlite")
        .build()
    )
```

Explore the categories to see the detailed specifications, models, and public APIs available!
