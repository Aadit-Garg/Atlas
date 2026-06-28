# Roles

**Roles** are metadata tags applied to Workers.

Roles MUST NOT change runtime execution behavior. The Atlas Runtime treats all Workers equally regardless of their Role.

## Purpose of Roles
Roles are primarily consumed by the ecosystem tooling:
- **Solon:** The developer toolchain (e.g., for generating specific scaffolding).
- **Atlas Studio:** For UI visualization and grouping.
- **Documentation:** For code generation and conceptual organization.
- **Testing:** For categorizing test suites.

### Indirect Ecosystem Significance
Although the Core Runtime ignores Roles during Invocation routing, Roles have massive **indirect significance**. 

Because Solon and Atlas Studio rely on Roles to understand the architecture of your application, mislabeling a Role will severely impact the developer experience. For example, if you tag a UI component with the `database` role, Solon will generate incorrect scaffolding (assuming it implements `StorageModel`), and Varsity will flag the architecture as a violation. Roles are the primary way Atlas enforces semantic correctness in the ecosystem.

## Common Roles

- `manager`: A Worker that orchestrates other Workers (e.g., Life, Scholar). Managers exist primarily for organization and Solon tooling.
- `database`: A Worker providing persistent data storage (e.g., SQLite, Postgres).
- `storage`: A Worker providing object or file storage.
- `cache`: A Worker providing ephemeral key-value storage.
- `ai`: A Worker providing language model or inference capabilities.
- `network`: A Worker handling external communication (e.g., HTTP clients, webhooks).
- `widget`: A Worker primarily focused on exporting UI capabilities.

*Note: A Worker may define one or multiple Roles simultaneously.*
