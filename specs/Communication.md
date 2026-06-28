# Communication

Atlas separates the **Control Plane** from the **Data Plane**.

## The Control Plane (Atlas)
Atlas is responsible for discovery, compatibility validation, permission negotiation, session establishment, and binding.

Atlas **MUST NOT** become the message broker.

## The Data Plane (Workers)
Once Atlas successfully binds a Capability request from Worker A to a Capability exported by Worker B, **Workers communicate directly**.

### P2P Communication
- **State Ownership:** Workers own their own business state and persistence.
- **Direct Invocation:** Method calls, RPC, or direct memory exchanges happen directly between the established Session endpoints.
- **Eventing:** If a Worker subscribes to an Event exported by another Worker, the subscription binding is negotiated by Atlas, but the delivery of the event is direct or handled via a dedicated `message-broker` Role Worker (not the Atlas kernel).

This guarantees that the Atlas Runtime remains extremely small, fast, and unburdened by business data routing.
