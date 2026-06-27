# Architecture

Status: Draft

Version: 0.1

---

# Purpose

This document defines the high-level architecture of Atlas.

All implementations must conform to this architecture.

---

# Design Goals

Atlas should be:

* Modular
* Extensible
* Local-first
* AI-native
* Event-driven
* Provider-based
* Application-agnostic

---

# Architectural Layers

Atlas consists of the following layers:

Application Layer

↓

Module Layer

↓

Core Runtime

↓

Capability Interfaces

↓

Provider Layer

↓

External Systems

---

# Layer Responsibilities

## Applications

Applications define user experiences.

Examples:

* LifeOS
* StudentOS
* CreatorOS

Applications assemble modules and configure providers.

---

## Modules

Modules implement business functionality.

Examples:

* Health
* Finance
* Reading
* Projects
* Journal

Modules never directly communicate with external systems.

Modules communicate only through:

* Events
* Capability Interfaces

---

## Core Runtime

The runtime is responsible for:

* Bootstrapping
* Dependency resolution
* Event dispatching
* Module lifecycle
* Provider lifecycle
* Configuration
* Scheduling
* Logging

The runtime contains no business logic.

---

## Capability Interfaces

Capabilities define what services exist.

Examples:

* Storage
* AI
* Notifications
* Authentication
* Search

Capabilities define interfaces only.

They contain no implementation.

---

## Providers

Providers implement capability interfaces.

Examples:

Storage

* SQLite
* PostgreSQL
* Google Sheets

AI

* Gemini
* Claude
* OpenAI
* Ollama

Providers should be interchangeable.

---

# Design Rules

The Core must never depend on a Module.

Modules must never depend on another Module directly.

Modules must communicate through Events.

Providers must implement Capability Interfaces.

Applications assemble Modules and Providers.

Business logic belongs inside Modules.

Infrastructure logic belongs inside Providers.

---

# Future Expansion

Atlas should support:

* Plugin system
* Marketplace
* Remote synchronization
* Cloud services
* Multiple applications
* Community modules

No architectural decisions should prevent future expansion.

---

# Success Criteria

Atlas succeeds if:

* New Modules can be added without changing Core.
* New Providers can be added without changing Modules.
* Applications can switch Providers without changing business logic.
* Features remain loosely coupled.
* Documentation remains the single source of truth.
