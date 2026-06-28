# Capabilities

Capabilities represent the abstract functionality required by a Worker. They are the currency of dependency resolution in Atlas.

## Capability Resolution Flow

When **Worker A** needs to save data:
1. **Worker A** emits a Header requesting the Capability (e.g., `capability.storage.sql`).
2. **Atlas (Room Steward)** reads this Header and checks the Global Registry for any Worker exporting that Capability.
3. Atlas decides (based purely on Metadata) whether to spawn a new Room or establish a direct Session within the current Room.
4. Atlas handles the Transport and Translation layers.
5. **Worker A** sends an **Invocation** over the Session.
6. The target Worker executes the Invocation.

## Exports vs Imports

Workers explicitly declare what they provide and what they need in their Manifest:

- **Imports:** The Capabilities required to function.
- **Exports:** 
  - **Services:** RPC endpoints or method invocations.
  - **Widgets:** UI components exposed for Atlas Studio.
  - **Events:** Subscribable triggers.
  - **Commands:** CLI actions.
