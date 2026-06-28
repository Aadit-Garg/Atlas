# Capabilities

Capabilities represent the abstract functionality required by a Worker. They are the currency of dependency resolution in Atlas.

## Capability Resolution Flow

When **Worker A** needs to save data, it doesn't import a specific database Worker. Instead:

1. **Worker A** requests a Capability (e.g., `capability.storage.sql`).
2. The Capability definition is defined in a **Model**.
3. **Atlas Runtime** looks in the Registry for any **Worker B** that explicitly implements that Model/Capability.
4. Atlas resolves the dependency, negotiates permissions, and creates a Session binding.
5. Worker A communicates directly with Worker B via the returned binding.

## Exports vs Imports

Workers explicitly declare what they provide and what they need in their Manifest:

- **Imports:** The Capabilities required to function.
- **Exports:** 
  - **Services:** RPC endpoints, classes, or direct invocation handles.
  - **Widgets:** UI components exposed for Atlas Studio.
  - **Events:** Pub/sub channels that other Workers can subscribe to (negotiated by Atlas, but routed directly or via a message-broker Worker).
  - **Commands:** CLI actions.
