# The Model System

Atlas relies heavily on **Models** to enforce consistency without enforcing implementation details.

## Why Models?

In many frameworks, standard behaviors are enforced via deep class inheritance from the core kernel. In Atlas, the core kernel (Runtime) is completely ignorant of business logic. 

Instead, standardization is achieved through **Models**.

A Model acts as a blueprint. It defines:
- The interfaces a Capability requires.
- The schemas of the data moving in and out.
- The events published.

By decoupling the Model from the Worker, tools like **Solon** can generate test mocks, SDKs, and UI scaffolding automatically, without ever needing to spin up the actual database or AI engine that implements the Model.

*(See `specs/Models.md` for full details).*
