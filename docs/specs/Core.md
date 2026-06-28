# Atlas Core

Atlas Core is the framework kernel.

Core owns exactly one thing: **Execution Orchestration**.

## Responsibilities

Core is strictly limited to:
- **Global Registry Management:** Maintaining runtime facts.
- **Room Stewardship:** Creating execution contexts and acting as the Steward inside those Rooms.
- **Discovery:** Finding installed Workers and Models.
- **Resolution:** Matching Capability requests using metadata.
- **Session Establishment:** Handling the 3 layers of communication (Communication, Transport, Translation).
- **Lifecycle:** Managing states for Workers and Rooms.

## Anti-Responsibilities

Core **MUST NOT**:
- Store persistent business data.
- Execute business logic or domain rules.
- Guess or infer sharing (always follows Metadata).
- Care about the programming language of the Worker.
