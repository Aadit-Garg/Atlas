# Modules

Status: Draft

Version: 0.1

---

# Purpose

Modules are self-contained units of business functionality.

They define the behavior of an Atlas application.

Examples include:

* Health
* Finance
* Reading
* Projects
* Journal
* Calendar

The Core Runtime should never contain business logic.

Business logic belongs inside Modules.

---

# Responsibilities

A Module may provide:

* Business logic
* Database models
* Event handlers
* Widgets
* Automation
* AI integrations
* Configuration
* APIs

Modules should not directly communicate with external systems.

---

# Module Structure

Every Module should contain:

README.md

manifest.yaml

database/

events/

automation/

widgets/

api/

ai/

tests/

docs/

assets/

---

# Manifest

Every Module must provide a manifest.

The manifest declares:

* ID
* Name
* Version
* Description
* Dependencies
* Required Capabilities
* Required Providers
* Permissions
* Events
* Widgets

Atlas uses the manifest to discover Modules.

---

# Communication

Modules communicate only through:

* Events
* Capability Interfaces

Modules must never directly call another Module.

This ensures loose coupling.

---

# Dependencies

A Module may depend on:

* Core Runtime
* Capability Interfaces

A Module may optionally depend on another Module through declared interfaces only.

Hidden dependencies are prohibited.

---

# Lifecycle

Each Module follows the Runtime lifecycle:

Registered

↓

Initialized

↓

Started

↓

Running

↓

Stopped

↓

Disposed

---

# Configuration

Every Module owns its own configuration.

Default settings should be provided.

Applications may override these settings.

---

# Events

Modules may:

Publish Events

Subscribe to Events

Ignore Events

Events should be treated as immutable.

---

# Permissions

Modules should request only the permissions they require.

Example:

* storage.read
* storage.write
* ai.generate
* notifications.send

Unused permissions should never be requested.

---

# Design Rules

Modules must:

* Be independent
* Be reusable
* Be testable
* Avoid side effects
* Minimize dependencies

Modules should be installable or removable without affecting unrelated Modules.

---

# Future

Modules should eventually support:

* Dynamic installation
* Marketplace distribution
* Version compatibility
* Hot reloading
* Third-party extensions