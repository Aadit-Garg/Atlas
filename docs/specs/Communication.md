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

### Unsatisfied Capabilities
Atlas evaluates the Header during Binding negotiation.
- **Required:** If a Required capability cannot be satisfied (e.g., no Provider exists), Atlas **Fails Fast** and prevents the requesting Worker from starting or joining the Room.
- **Optional:** If an Optional capability cannot be satisfied, the Worker starts normally, but the Binding is marked as `FAILED`. Any attempt to invoke it will return a `CapabilityUnavailable` error, allowing the Worker to degrade gracefully.

### Rooms vs. Direct Sessions
Atlas reads the metadata and decides whether to create a new Room for this collaboration, or simply create direct Sessions. **This decision is 100% metadata-driven and never heuristic.**

The decision rules are as follows:
- **Direct Session:** Used when two Workers require isolated, point-to-point communication with no shared state cache (e.g., a simple API request).
- **Room:** A Room is instantiated when:
  1. Three or more Workers need to collaborate in a single lifecycle boundary.
  2. The Workers need to share a synchronized execution cache (the Room Registry).
  3. Observers or Telemetry Workers are declared, requiring a dedicated scope to monitor the Invocations without polluting global traffic.

## Sessions
Sessions remain the fundamental communication primitive. **Rooms DO NOT replace Sessions.** 
Workers use Sessions. Miron uses Sessions. Solon uses Sessions. Sessions exist *inside* Rooms.
