# Models

> Every project accumulates a few stories.
>
> During Atlas' design, Models were briefly called "Hookers" because they connected Workers to standardized behaviour.
>
> The idea lasted approximately one conversation before everyone realized introducing Atlas with "Workers implement Hookers" was probably not ideal.
>
> The name was retired.
>
> Models are now the authoritative specification Workers implement.
>
> The joke remains part of Atlas lore.

<details>
<summary>The Lore</summary>
The term was initially coined because the framework needed a way to "hook" standalone code into a larger operating system context. The engineering team jokingly referred to the declarative rulesets as "Hookers". It was dropped instantly once the marketing implications were discussed, but the "Hooker" naming survives as an internal easter egg.
</details>

---

## What is a Model?

A **Model** is the ideal, tool-independent specification that Workers implement. 

Models are **NOT** executable. They are declarative definitions. Multiple tools must be able to consume Models (e.g., Solon, Atlas Studio, the Runtime).

### Contents of a Model
A Model may define:
- **Interface Definitions:** The Python `typing.Protocol` or RPC schemas expected.
- **Schemas:** Data shapes for inputs, outputs, and storage.
- **Lifecycle Expectations:** Startup, shutdown, and pause states.
- **Permissions:** Data access scopes required by the Model.
- **Events:** The exact payload schemas of events published.
- **Compatibility Rules:** Constraints on runtime execution.
- **Widgets:** UI definitions that Workers implementing the Model must export.
- **Generators/Tests:** Used by Solon to generate scaffolding and mocks.

## The Rule of Ownership
- **Workers implement Models.**
- **Workers NEVER own Models.**

Models exist independently of any implementation. This allows the Solon developer toolchain to validate any Worker against a Model without executing the Worker itself.

## Model Versioning Policy

Because Models are contracts between independent Workers, they must be strictly versioned using Semantic Versioning (e.g., `v1.0.0`).

### Compatibility Rules
- **Minor Version Bumps (e.g., `v1.0` -> `v1.1`):** Indicate backward-compatible additions (e.g., a new optional capability or event). A Worker requiring `v1.0` can safely bind to a Provider exporting `v1.1`.
- **Major Version Bumps (e.g., `v1.0` -> `v2.0`):** Indicate breaking changes to the contract (e.g., changing input schemas, dropping a capability). A Worker requiring `v1.0` **will not bind** to a Provider exporting `v2.0` unless a backward-compatibility Adapter (Translator) is explicitly declared.

If a Standard Model evolves and introduces a breaking change, ecosystem stability is preserved because the Runtime enforces these strict version boundaries during Binding negotiation.
