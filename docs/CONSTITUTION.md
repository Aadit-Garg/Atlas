# Atlas Constitution

This document defines the foundational laws of the Atlas Software Platform.

Every architectural decision, every runtime implementation, and every product built upon Atlas must adhere to these principles. If an implementation violates these rules, it is invalid.

## 1. Atlas Coordinates. Workers Execute.
Atlas is a Control Plane. It discovers, binds, and manages lifecycles. It never executes business logic. **Workers** are the only executable primitives. 

## 2. Rooms Define Collaboration.
A Room is an execution context, not a container. When Workers need to collaborate, they do so within a Room. Rooms contain a localized Registry and are stewarded by Atlas. 

## 3. Models Define Behavior.
Workers do not guess how to communicate. **Models** are the declarative, tool-independent specifications that dictate capabilities, schemas, and expectations. 

## 4. Atlas Never Guesses.
Atlas executes declared intent. Every runtime decision—from scheduling to resource sharing to Room creation—must be explainable through metadata. Atlas never infers sharing or clones Workers automatically.

## 5. Metadata Drives Runtime.
The Global Registry and Room Registries store runtime facts (e.g., active Bindings, running Workers). **No business state should ever exist inside Atlas or its Registries.**

## 6. Language Neutrality is Mandatory.
Python is merely an implementation detail. The execution model is language-agnostic. Workers may be written in any language (Rust, Go, C++, Zig) and must interoperate through the three independent communication layers: Communication, Transport, and Translation.

## 7. The Primitives are Frozen.
The core primitives are: **Worker, Room, Session, Registry, Binding, Invocation**. No new runtime concepts may be introduced unless they resolve a demonstrable architectural flaw that cannot be expressed using these primitives, and only after passing an Architecture Decision Record (ADR).
