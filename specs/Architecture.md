# Architecture

Atlas employs a strictly segregated Control Plane vs Data Plane architecture.

```text
Solon Toolchain (Tooling)
↓
Models (Declarative Specs)
↓
Workers (Executable Implementations)
```

## 1. Solon
Solon is the Atlas developer toolchain. It consumes **Models**, validates **Workers**, and generates tests, SDKs, and dependency graphs. It never runs in production.

## 2. Models
Models are the ideal, tool-independent specifications that dictate how a Capability should behave, what events it fires, and what its schemas look like.

## 3. Workers
Workers are the **ONLY** executable primitive. They implement Models. 

There is no distinction between an "Application", a "Provider", or a "Module". A Worker is simply an independent, executable package that can:
- Export Capabilities (Services, Widgets, Events)
- Import Capabilities
- Manage its own state and storage

## 4. The Runtime (Control Plane)
The Atlas Runtime is deliberately minimal. It handles:
- **Discovery:** Finding installed Workers and Models.
- **Resolution:** Matching Worker capability requests to Worker exports.
- **Session/Binding:** Establishing permissions and creating the binding between two Workers.
- **Lifecycle:** Starting and stopping Workers.

Atlas **does not** broker messages, store application data, or execute business logic.

## 5. The Data Plane
Once Atlas binds two Workers together, they communicate directly via the established Session. Workers own their Data Plane.
