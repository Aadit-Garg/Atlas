# Naming History

As with any evolving architecture, terminology in Atlas has undergone several iterations to improve conceptual clarity. 

This document records the major naming shifts to help contextualize older documentation or discussions.

## Applications & Providers → Workers
Early in Atlas' design, there was a strict architectural split between "Applications" (which held business logic and UI) and "Providers" (which held infrastructure like databases). 

It was eventually realized that this distinction forced arbitrary limits. An Application might need to provide a capability to another Application. A Provider might need a UI Widget for configuration.

The concepts were merged into the singular **Worker**. A Worker is the only executable primitive. Whether a Worker acts like a user-facing Application or a background database is purely a matter of its **Roles** metadata.

## Rulesets → Models
Originally, the declarative blueprints for Capabilities were called "Rulesets". This was renamed to **Models** to better reflect that they model data structures, interfaces, and expected behaviors, rather than just "rules".

## Manager (from Primitive to Role)
Early designs treated a "Manager" (like Life or Scholar) as a special runtime primitive that sat above Applications. This introduced unnecessary complexity into the Runtime.

The Runtime was simplified. A Manager is now simply a normal Worker that happens to have the metadata Role `manager`. It orchestrates other Workers using standard Capability imports, removing the need for the Runtime to treat it uniquely.

## Models → Capability & Resource Models
As Atlas evolved its Translation Layer to seamlessly bridge multi-language Workers, a critical distinction emerged. Calling everything a "Model" conflated behavior with data structures.

To fix this, the concept was formally split:
- **Capability Models** define behavior (verbs).
- **Resource Models** define canonical data structures (nouns).

This distinction allowed the Translation Layer to use Resource Models as canonical targets for serialization, massively simplifying cross-language data exchange.
