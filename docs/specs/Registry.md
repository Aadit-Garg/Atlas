# Registry

The Registry in Atlas is split into two distinct tiers: The **Global Registry** and the **Room Registry**. 

Neither Registry is a database. They store **runtime facts only**. Nothing related to business state should ever exist inside a Registry.

## 1. The Global Registry
The Global Registry is the central source of truth for the entire Atlas Runtime. It tracks the macro-state of the platform.

**Stores:**
- Running Workers
- Running Rooms
- Available Models
- Capabilities
- Health metrics
- Global Bindings

## 2. The Room Registry
Every Room owns a local Registry, managed by the Room Steward. 

The Room Registry functions as an **execution cache**. Workers inside the Room communicate through this local Registry rather than repeatedly querying the Global Registry, ensuring massive scalability and reducing locks.

**Stores:**
- Room Participants (Workers bound to the Room)
- Participant Bindings
- Communication Table (Header routing)
- Transport Table (e.g., TCP, Unix Socket mapping)
- Translation Table (e.g., Python to Rust serializers)
- Active Invocations
- Outstanding Requests & Pending Responses
- Room-local lifecycle information and metrics
