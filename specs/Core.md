# Core

Status: Draft

Version: 0.1

---

# Purpose

Atlas Core is the foundation of the Atlas platform.

It provides the infrastructure required to execute Applications, Modules, and Providers.

Core contains no business logic.

---

# Responsibilities

Atlas Core is responsible for:

* Runtime
* Registry
* Event Bus
* Capability Resolution
* Configuration
* Lifecycle
* Logging
* Diagnostics
* Scheduling

Core coordinates execution.

It does not implement features.

---

# Public Components

Atlas Core exposes:

* Runtime
* Event Bus
* Registry
* Capability Registry
* Configuration Manager
* Lifecycle Manager

These are considered stable APIs.

---

# Internal Components

Internal implementation details are not accessible to Modules.

Examples:

* Internal caches
* Boot helpers
* Runtime internals
* Dependency resolver

Internal APIs may change without notice.

---

# Dependency Rules

Core depends on nothing except shared libraries.

Modules depend on Core.

Providers depend on Core.

Applications depend on Core.

Core must never depend on Modules.

Core must never depend on Providers.

---

# Stability

Core APIs should remain stable.

Breaking changes require:

* Version increase
* Migration guide
* Deprecation period

---

# Design Rules

Core must be:

* Minimal
* Stable
* Framework independent
* Provider independent
* Module independent
* Testable

---

# Future

Future versions may include:

* Distributed Runtime
* Multi-process execution
* Remote modules
* Sandboxed plugins
