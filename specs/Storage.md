# Storage

Status: Draft

Version: 0.1

---

# Purpose

The Storage layer provides persistent data management for Atlas.

Storage is accessed exclusively through the Storage Capability.

No Module may communicate directly with a database.

---

# Goals

* Storage provider independence.
* ACID support where available.
* Replaceable implementations.
* Offline-first.
* Secure by default.
* Migration support.

---

# Design Principles

Storage is a Capability.

Providers implement Storage.

Modules consume Storage.

Applications configure Storage.

---

# Responsibilities

The Storage layer is responsible for:

* Persisting data
* Querying data
* Updating data
* Deleting data
* Transactions
* Backups
* Migrations
* Version compatibility

---

# Supported Providers

Initial providers:

* SQLite
* PostgreSQL
* Google Sheets
* Atlas Cloud

Future providers:

* MongoDB
* MySQL
* CSV
* JSON
* Supabase

---

# Storage Operations

Every Storage Provider must support:

* Create
* Read
* Update
* Delete
* Query

Optional:

* Transactions
* Batch Operations
* Full-text Search
* Streaming

---

# Transactions

Providers should support transactions whenever possible.

If unsupported, Providers must document the limitation.

The Runtime should adapt accordingly.

---

# Identifiers

Every stored object must have a globally unique identifier.

IDs must never be reused.

---

# Versioning

Storage Providers declare:

* Schema Version
* Provider Version
* Migration Version

Runtime validates compatibility before startup.

---

# Design Rules

Storage Providers must:

* Never contain business logic.
* Never expose implementation-specific APIs.
* Validate data before persistence.
* Produce meaningful errors.
* Support backups.

---

# Future

Planned features:

* Encryption
* Compression
* Distributed storage
* Read replicas
* Remote synchronization
