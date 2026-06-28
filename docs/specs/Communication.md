# Communication

Atlas completely separates communication into three independent layers. Atlas owns all three layers.

## The Three Layers

1. **Communication (Who is talking)**
   Defines the logical source and destination, governed by Models and capabilities.
2. **Transport (How bytes move)**
   The physical layer of data transfer. Supported transports remain pluggable (e.g., Shared Memory, TCP, Unix Sockets, Named Pipes, CAN, I2C). Future transports must be implementable without changing Worker APIs.
3. **Translation (How runtimes understand each other)**
   Because Atlas is language-neutral, Workers written in different languages require translation. Atlas manages the serialization/deserialization between language runtimes.

## Header-Based Routing

Workers communicate by sending a **Header**. The Header describes the intent of the communication request. It may describe multiple requests simultaneously.

**Example Header:**
```yaml
Required:
  - capability.storage.database
Optional:
  - capability.analytics.telemetry
```

Atlas (the Room Steward) reads this metadata and decides whether to create a new Room for this collaboration, or simply create direct Sessions. **This decision is 100% metadata-driven and never heuristic.**

## Sessions
Sessions remain the fundamental communication primitive. **Rooms DO NOT replace Sessions.** 
Workers use Sessions. Miron uses Sessions. Solon uses Sessions. Sessions exist *inside* Rooms.
