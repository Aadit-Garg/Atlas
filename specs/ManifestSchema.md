# Worker Manifest Schema

Every Worker must provide a `worker.yaml` file (or equivalent manifest) to declare its identity, Roles, Imports, and Exports.

This replaces the older concepts of `module.yaml` and `provider.yaml`.

## Schema Draft

```yaml
version: "1.0"

worker:
  id: string              # e.g. "atlas.worker.sqlite"
  name: string            # Human readable name
  version: string         # SemVer string
  roles:                  # Metadata tags for Solon / Studio
    - string              # e.g. "database", "storage", "manager"

imports:                  # Capabilities this Worker requires
  capabilities:
    - name: string        # Capability identity (e.g., "storage.sql")
      version: string     # Expected Model version
      optional: boolean   # Default: false
      reason: string      # Why it needs this

exports:                  # Capabilities this Worker provides
  capabilities:
    - name: string        # Capability identity
      version: string     # Implemented Model version

  widgets:                # UI components exported
    - id: string
      name: string

  events:                 # Events this Worker publishes
    - id: string
      schema: string      # Reference to schema definition
```

## Validation

The Solon toolchain uses this manifest to validate the Worker, generate mock tests for its imports, and ensure it correctly implements the Models for its exports. The Atlas Runtime uses this manifest during Boot for Discovery and Registration.
