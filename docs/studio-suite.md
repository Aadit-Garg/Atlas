# Atlas Studio Suite

The Atlas Studio Suite is the official developer toolkit and ecosystem for the Atlas platform. 

Atlas itself is just the execution model (the Runtime). To build, validate, and manage software effectively on Atlas, developers use the Studio Suite. The Suite is designed as an ecosystem of distinct tools, each handling a specific phase of the software lifecycle.

## Atlas Studio (Workspace Manager)

**Atlas Studio** is the primary visual entry point into the Atlas ecosystem. It is a powerful authoring and composition environment built specifically for modular software architecture.
*(Conceptual equivalent: Visual Studio Code + Unreal Engine Blueprints).*

Architecturally, Atlas Studio is a Manager application. Its responsibility is to organize projects, environments, and downloaded dependencies before the Runtime is even booted for a specific project.

**Core Features:**
- **Visual Topology Designer:** Drag and drop Workers onto a visual canvas to wire up architecture without writing Python `ManagerBuilder` scripts. Studio visually flags missing dependencies and auto-generates the declarative `atlas.yaml`.
- **Integrated Marketplace:** A 1-click package manager for the Atlas ecosystem. Browse and install community Workers, Standard Models, and Translators directly from the global Registry into your workspace.
- **Environment & Profile Management:** Define configuration profiles (e.g., `dev`, `staging`) to seamlessly inject different `ConfigModel` values and API keys across all Workers in your workspace instantly.
- **Cross-Language Toolchain Orchestration:** Atlas supports multi-language projects. Studio automatically detects manifest languages and transparently manages the underlying toolchains (like Rust `cargo` or Node `npm`) so you don't have to.
- **Project Scaffolding:** Create new Workspaces via visual wizards (a GUI over the underlying `atlas new` CLI).

## Miron (Runtime Console)

**Miron** is the visual runtime console for Atlas. 
*(Conceptual equivalent: Task Manager + Docker Desktop + Runtime Inspector).*

Architecturally, **Miron is a Worker**. It is not a special runtime primitive. It uses standard Sessions (with upgraded Observer privileges) to inspect and manage other Workers and Rooms.

**Responsibilities:**
- Inspect running Workers in real-time.
- Monitor Data Plane communication and Session health.
- View the active Registry (what Capabilities are bound to what).
- Visualize the runtime topology (dependency graphs).
- Suspend Rooms and pause, stop, or manage running Workers (acting as a Task Manager).

## Solon (The Toolchain)

**Solon** is the build system and static validator for Atlas.
*(Conceptual equivalent: The Rust `cargo` CLI + OpenAPI generators).*

**Responsibilities:**
- Validate Worker manifests against Model specifications.
- Generate test mocks for Capabilities.
- Generate Python SDKs and interface stubs from YAML Models.
- Validate architectural compliance without booting the Runtime.

*Example commands:*
- `solon build`
- `solon test sqlite`
- `solon validate`
- `solon docs`

## Varsity (The Mentor)

**Varsity** is the learning platform and scaffolding engine.
*(Conceptual equivalent: interactive tutorials + project generators).*

**Responsibilities:**
- Provide interactive tutorials on Atlas architecture.
- Scaffold new Workers and Models using best practices.
- Act as an architecture mentor, reviewing project structures.
- Recommend standard patterns and predefined Roles.

## Future Extensibility

The Studio Suite is not a single, monolithic application. It is an ecosystem. Future applications (like visual node-editors for routing Events, or marketplace managers) will fit naturally into this suite, leveraging the standardized Model format.
