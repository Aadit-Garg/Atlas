# Networking Workers

The **Networking** category abstracts network protocols, allowing Atlas applications to communicate with the outside world, fetch data, and serve clients.

---

## HTTP Client (`atlas.network.http_client`)

**Purpose:** Fetches data from remote REST APIs and web servers.
**Implemented Model:** `HttpClientModel`
**Roles:** `[network, client]`

### Public APIs
- `request(method: str, url: str, headers: dict = None, body: str = None) -> dict` (Returns status code, headers, and body).
- `get(url: str) -> dict`
- `post(url: str, body: str) -> dict`

### Dependencies
- Often depends on `atlas.core.logger` to record failed requests.

### Failure Modes
Must handle timeouts, DNS resolution failures, and connection drops gracefully. Should return a structured error dictionary rather than throwing an unhandled exception.

---

## HTTP Server (`atlas.network.http_server`)

**Purpose:** Serves incoming HTTP requests, allowing an Atlas Manager to act as a web backend.
**Implemented Model:** `HttpServerModel`
**Roles:** `[network, server]`

### Public APIs
- `start(port: int) -> None`
- `stop() -> None`
- `register_route(method: str, path: str, handler_capability: str) -> None`

### Integration with Atlas
When a request hits a registered route, the `http_server` worker translates the HTTP request into an Atlas **Invocation** and sends it to the specified `handler_capability`. 

For example, `GET /users` might trigger the `atlas.my_app.get_users` capability on another worker. The server waits for the response and translates it back into an HTTP 200 OK.

---

## WebSocket Client & Server (`atlas.network.websocket_*`)

**Purpose:** Full-duplex communication for real-time applications (chat, live dashboards).
**Implemented Model:** `WebSocketClientModel`, `WebSocketServerModel`
**Roles:** `[network]`

### Public APIs (Client)
- `connect(url: str) -> bool`
- `send(message: str) -> None`
- `on_message(handler_capability: str) -> None`

### Usage
Like the HTTP Server, WebSocket workers bridge the outside world with internal Atlas capabilities. When a message arrives, the worker invokes the registered handler capability.

---

## Other Proposed Networking Workers

- **TCP/UDP:** Low-level socket programming models for custom protocols.
- **MQTT:** IoT messaging protocol, crucial for hardware and robotics managers.
- **DNS:** Utility for resolving domain names to IP addresses without relying strictly on the OS default behavior (useful for custom routing).
