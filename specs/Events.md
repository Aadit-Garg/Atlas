# Events

Status: Draft

Version: 0.1

---

# Purpose

Events are Atlas' communication mechanism.

Modules communicate through Events rather than direct function calls.

This minimizes coupling and improves extensibility.

---

# Philosophy

Instead of:

Health → Dashboard

Health → Analytics

Health → Achievements

Health → AI

Health publishes an Event.

Interested components respond independently.

---

# Event Bus

The Runtime owns a single Event Bus.

The Event Bus is responsible for:

* Publishing Events
* Delivering Events
* Managing Subscribers
* Error Isolation
* Logging

---

# Event Lifecycle

Publisher

↓

Event Bus

↓

Subscribers

↓

Completion

The Publisher does not know who receives the Event.

Subscribers do not know who published it.

---

# Event Naming

Events should use the format:

Domain.Action

Examples:

Health.WorkoutCompleted

Finance.ExpenseAdded

Tasks.TaskCompleted

Journal.EntryCreated

Reading.BookFinished

System.StartupCompleted

---

# Event Structure

Every Event contains:

* Event ID
* Name
* Timestamp
* Source
* Payload
* Metadata
* Version

Payloads should be immutable.

---

# Event Types

System

Module

Provider

Application

User

Internal

Future categories may be introduced.

---

# Subscription

Components subscribe to Events they care about.

Subscriptions should be declared during initialization.

The Runtime manages all subscriptions.

---

# Error Handling

Subscriber failures must not stop Event delivery.

The Event Bus should:

Log the failure.

Continue delivering the Event to remaining subscribers.

---

# Ordering

Events should be processed in publish order unless explicitly documented otherwise.

Long-running Event handlers should execute asynchronously when supported.

---

# Event History

The Runtime may optionally record Event history for:

Debugging

Analytics

Replay

Auditing

Storage of Event history is implementation-specific.

---

# Design Rules

Events must:

* Represent completed actions.
* Be immutable.
* Be versioned.
* Avoid large payloads.
* Be descriptive.

Events must never expose implementation details.

---

# Examples

Health.WorkoutCompleted

↓

XP Module

↓

Analytics Module

↓

Achievements Module

↓

AI Module

↓

Notification Module

Each reacts independently.

---

# Future

Potential future enhancements:

* Event replay
* Distributed Event Bus
* Remote subscribers
* Event priorities
* Scheduled Events
* Event persistence
