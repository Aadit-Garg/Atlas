# Atlas

> **Atlas is a modular framework for building Personal Operating Systems.**

LifeOS is the first application built using Atlas.

## Fun Fact

During Atlas' design, the Model system almost had a very different name.

For roughly one design session it was internally called **Hookers**, because they "hooked" Workers to standardized behavior.

That idea survived exactly until someone pointed out what "hooker" usually means in English.

The name was immediately retired.

Models were born.

The joke, however, became part of Atlas history.

---

# What is Atlas?

Atlas is not a productivity app.

Atlas is not a habit tracker.

Atlas is not a Google Sheets template.

Atlas is a framework that allows developers to build highly customizable personal operating systems.

An Atlas application can help users manage their health, finances, learning, projects, schedules, and personal knowledge while remaining completely modular and extensible.

---

# Philosophy

Atlas follows a few core principles:

* Core should know as little as possible.
* Everything is modular.
* Everything external is a Provider.
* Communication happens through Events.
* Applications are built from Modules.
* AI is a first-class citizen.
* Storage is replaceable.
* Local-first whenever possible.
* Documentation is the source of truth.

---

# Core Concepts

## Core

The runtime that powers every Atlas application.

## Modules

Business functionality such as Health, Finance, Reading, Projects, Calendar, or Journal.

## Providers

Interfaces to external systems such as SQLite, PostgreSQL, Google Sheets, Gemini, Claude, or Email.

## Applications

Complete products built using Atlas.

Example:

* LifeOS
* StudentOS
* CreatorOS

---

# Repository Structure

/specs

Engineering specifications.

Source of truth.

---

/packages

Reusable framework packages.

---

/runtime

Atlas runtime and lifecycle.

---

/modules

Business modules.

---

/providers

External integrations.

---

/apps

Applications built using Atlas.

---

/sdk

Developer SDK.

---

/tools

Internal developer tooling.

---

# Current Goal

Build Atlas Core.

Once Atlas Core is stable, build LifeOS as the reference implementation.

---

# Development Philosophy

Architecture First.

Implementation Second.

Optimization Last.

Every implementation should be derived from the specifications contained inside `/specs`.

Never implement features before they are architecturally defined.

---

# Long-Term Vision

Atlas should eventually support:

* Local desktop applications
* Web applications
* Mobile applications
* Self-hosted deployments
* Managed cloud deployments
* Multiple storage providers
* Multiple AI providers
* Third-party modules
* Community extensions

---

# License

TBD
