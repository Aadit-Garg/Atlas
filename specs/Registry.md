# Registry

Status: Draft

Version: 0.1

---

# Purpose

The Registry is Atlas' discovery mechanism.

It stores everything currently available inside the Runtime.

---

# Responsibilities

The Registry tracks:

Applications

Modules

Providers

Capabilities

Interfaces

Events

Widgets

Commands

Themes

---

# Discovery

During startup:

Providers register.

Modules register.

Capabilities register.

Applications register.

The Runtime validates all registrations.

---

# Lookups

Components should discover dependencies through the Registry.

Hardcoded references are prohibited.

---

# Validation

The Registry validates:

Unique IDs

Versions

Compatibility

Dependencies

Permissions

---

# Dynamic Registration

Future versions may support:

* Hot loading
* Hot unloading
* Runtime discovery

---

# Design Rules

The Registry is read-only for consumers.

Only the Runtime may modify registrations.

---

# Future

Potential future additions:

* Plugin Registry
* Remote Registry
* Marketplace Registry
