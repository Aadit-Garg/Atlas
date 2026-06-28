# AI & Hardware Workers

The **AI & Hardware** category represents advanced Atlas capabilities. By standardizing these interfaces, Managers can easily swap between local models, cloud APIs, and physical hardware sensors without rewriting their domain logic.

---

## 1. AI Workers

### Prompt (`atlas.ai.prompt`)
**Purpose:** Formats context, instructions, and user input into standardized prompts.
**Implemented Model:** `PromptModel`

**Public APIs:**
- `format(template: str, variables: dict) -> str`
- `validate(prompt: str) -> bool`

### Tokenizer (`atlas.ai.tokenizer`)
**Purpose:** Counts and encodes text into tokens for AI models.
**Implemented Model:** `TokenizerModel`

**Public APIs:**
- `encode(text: str) -> list[int]`
- `decode(tokens: list[int]) -> str`
- `count(text: str) -> int`

### Embedding (`atlas.ai.embedding`)
**Purpose:** Converts text into numerical vectors for semantic search.
**Implemented Model:** `EmbeddingModel`

**Public APIs:**
- `embed(text: str) -> list[float]`
- `embed_batch(texts: list[str]) -> list[list[float]]`

### Inference (`atlas.ai.inference`)
**Purpose:** Generates text or actions from an LLM. Concrete implementations could wrap OpenAI, Anthropic, or local LLaMA models.
**Implemented Model:** `InferenceModel`

**Public APIs:**
- `generate(prompt: str, max_tokens: int) -> str`
- `stream(prompt: str) -> iter[str]`

### Vector Store (`atlas.ai.vector_store`)
**Purpose:** Specialized storage for semantic search.
**Implemented Model:** `VectorStoreModel`

**Public APIs:**
- `upsert(id: str, vector: list[float], metadata: dict) -> None`
- `search(vector: list[float], top_k: int) -> list[dict]`

---

## 2. Hardware Workers

Hardware workers provide standardized access to physical computing protocols, making Atlas an excellent foundation for robotics, IoT, and embedded systems.

### GPIO (`atlas.hardware.gpio`)
**Purpose:** Controls General Purpose Input/Output pins.
**Implemented Model:** `GPIOModel`

**Public APIs:**
- `setup(pin: int, mode: str) -> None`
- `write(pin: int, value: int) -> None`
- `read(pin: int) -> int`

### Serial, I2C, SPI, CAN
**Purpose:** Standard communication buses for interacting with microcontrollers and sensors.
**Implemented Model:** `BusModel`

**Public APIs:**
- `write(address: int, data: bytes) -> None`
- `read(address: int, length: int) -> bytes`

### Sensors (IMU, GPS)
**Purpose:** Reads physical location, acceleration, and orientation.
**Implemented Model:** `SensorModel`

**Public APIs:**
- `read_data() -> dict` (e.g., `{"latitude": 40.71, "longitude": -74.00}`)

### Actuators (Motor)
**Purpose:** Drives physical movement.
**Implemented Model:** `MotorModel`

**Public APIs:**
- `set_speed(speed: float) -> None`
- `stop() -> None`

### Wireless (Bluetooth, Wi-Fi)
**Purpose:** Scans and connects to wireless networks and BLE devices.
**Implemented Model:** `WirelessModel`

**Public APIs:**
- `scan() -> list[dict]`
- `connect(device_id: str) -> bool`
