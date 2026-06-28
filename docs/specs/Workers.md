# Workers

**Worker** is the ONLY executable primitive in the Atlas architecture.

Everything executable is a Worker. There is NO architectural distinction between "Applications", "Providers", or "Modules". 

## Examples of Workers
- SQLite (Storage Provider)
- Gemini (AI Provider)
- Journal (Stateful application feature)
- Task Manager
- Life (Manager)

## Core Responsibilities
Atlas coordinates; **Workers execute**.

Every Worker may:
- **Own State:** Workers manage their own business state and persistence.
- **Implement Models:** Workers implement the declarative behaviors defined in Models.
- **Export Capabilities:** Workers expose Services, Widgets, Commands, and Events.

Workers **never** own discovery, routing, or lifecycle coordination.

## Resource Sharing & Instantiation
Workers are globally managed by Atlas. Atlas never clones Workers automatically; it only follows declared execution metadata.

Worker sharing is determined by three levels of policy:
1. **Worker Policy:** Does the Worker allow itself to be shared? (e.g., Singleton vs Pool)
2. **Runtime Policy:** Does Atlas permit sharing globally?
3. **Room Policy:** Does the specific Room permit shared participants?

Only when all three permit sharing will Atlas reuse a Worker instance across multiple Rooms.

## Execution Model
Workers do not execute Sessions directly. Every request sent over a Session is translated by Atlas into an **Invocation**. 

Workers execute Invocations based on their scheduling metadata. 

## Language Neutrality
Workers may be implemented in **any programming language** (e.g., Python, Rust, Zig, Go). Language is purely an implementation detail. Workers advertise their supported transports, serializations, and runtime languages in their manifest, allowing Atlas to manage the translation layer during execution.
