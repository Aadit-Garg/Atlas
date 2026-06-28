# Binding

A **Binding** is a negotiated, persistent (within the scope of a Session) connection established by the Atlas Runtime between a Requester (the caller) and a Provider (the executor).

Bindings ensure that a Worker can confidently send an Invocation to another Capability without needing to know *where* it is or *what format* it speaks.

---

## Negotiation Semantics

When a Worker requires a Capability, Atlas does not simply connect the two ends. It performs a **Negotiation**.

1. **Discovery:** Atlas searches the Global Registry for a Provider exporting the requested Capability that satisfies the version constraints.
2. **Protocol Matching:** Atlas checks the `communication.transports` and `communication.formats` arrays of both the Requester and the Provider.
3. **Direct Match:** If both Workers share a transport (e.g., `memory`) and a format (e.g., `python`), the Binding is established directly.
4. **Translation Path:** If the Workers do not share a common format (e.g., Requester speaks `python`, Provider speaks `json`), Atlas searches for a Translator Worker. If a translation path exists, Atlas establishes a multi-step Binding, automatically inserting the Translator into the pipeline.

---

## Lifecycle

A Binding progresses through the following states:

1. `REQUESTED`: The Requester has declared the requirement, but Atlas has not yet evaluated it.
2. `NEGOTIATING`: Atlas is actively searching the Registry for Providers and calculating translation paths.
3. `ESTABLISHED`: A valid Provider and translation path have been found. The route is cached in the Room Registry.
4. `TERMINATED`: The Room or Session is destroyed, or the Provider is unloaded from the Global Registry.

---

## Failure Behavior

If negotiation fails, the failure must be handled deterministically.

- **Missing Provider:** If no Worker in the ecosystem exports the requested Capability, Atlas rejects the Binding.
- **No Translation Path:** If a Provider exists, but there is no way to translate the Requester's format into the Provider's format, Atlas rejects the Binding.
- **Fail Fast (Required):** If the Capability was listed as `Required` in the Requester's Manifest, Atlas will **prevent the Requester from starting** entirely.
- **Graceful Degradation (Optional):** If the Capability was listed as `Optional`, the Binding remains in a `FAILED` state. The Requester is allowed to start, but any attempt to send an Invocation over this Binding will immediately return a `CapabilityUnavailable` error header.

---

## The Source of Truth

Bindings are ephemeral. They are evaluated and created by the **Global Registry**, but the resulting negotiated routes are cached inside the **Room Registry** for high-speed Invocation routing during execution. If the Global Topology changes (e.g., a Provider goes offline), the Global Registry will force the Room Registry to invalidate and renegotiate the Binding.
