# Database

Status: Draft

Version: 0.1

---

# Purpose

The Database defines how Atlas stores structured information.

It is independent of any specific database technology.

---

# Philosophy

Atlas stores domain data.

Applications decide which Modules are enabled.

Modules define their own schemas.

Providers determine where the data is stored.

---

# Core Entities

Every Atlas installation contains:

Applications

Modules

Providers

Capabilities

Users

Settings

Events

Tasks

Projects

Logs

Additional entities may be introduced by Modules.

---

# Schema Ownership

Each Module owns its own schema.

Example

Health Module

↓

Health Tables

Finance Module

↓

Finance Tables

Projects Module

↓

Project Tables

Modules should never modify another Module's schema directly.

---

# Relationships

Modules may reference other Modules using identifiers only.

Direct table dependencies should be minimized.

---

# Naming

Entities should use singular names.

Examples:

Task

Workout

Expense

Project

JournalEntry

Avoid implementation-specific naming.

---

# Metadata

Every entity should include:

* ID
* Created At
* Updated At
* Version

Optional:

* Owner
* Tags
* Status
* Metadata

---

# Validation

Data validation occurs before persistence.

Validation rules belong to the owning Module.

Storage Providers enforce structural integrity.

---

# Evolution

Schema changes require migrations.

Breaking changes require a new schema version.

Backward compatibility should be maintained whenever practical.

---

# Import and Export

Atlas should support:

* Full export
* Module export
* Incremental backup
* Restore

Storage format depends on the selected Provider.

---

# Design Rules

The Database is:

* Modular
* Versioned
* Extensible
* Provider independent

Business logic must never reside inside the database.

---

# Future

Potential future enhancements:

* Schema registry
* Automatic indexing
* Cross-module references
* Graph relationships
* Search optimization
