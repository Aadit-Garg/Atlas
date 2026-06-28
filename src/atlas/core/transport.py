from abc import ABC, abstractmethod
from typing import Dict, Optional, Callable
from dataclasses import dataclass
import threading
import queue

from .diagnostics import Result, AtlasError, Severity

class TransportError(AtlasError):
    def __init__(self, message: str, context: Optional[Dict[str, str]] = None):
        super().__init__(code="ERR_TRANSPORT", severity=Severity.RECOVERABLE, message=message, context=context or {})

@dataclass(frozen=True)
class TransportPayload:
    """
    The fundamental unit of the Transport Layer.
    Contains strictly raw bytes. No capability semantics.
    """
    data: bytes

class TransportStrategy(ABC):
    """
    Abstract interface for moving bytes across channels.
    """
    @abstractmethod
    def create_channel(self, channel_id: str) -> Result[None, TransportError]:
        pass

    @abstractmethod
    def send(self, channel_id: str, data: bytes) -> Result[None, TransportError]:
        pass

    @abstractmethod
    def receive(self, channel_id: str, callback: Callable[[TransportPayload], None]) -> Result[None, TransportError]:
        pass
        
    @abstractmethod
    def close(self, channel_id: str) -> Result[None, TransportError]:
        pass


class InMemoryTransport(TransportStrategy):
    """
    Thread-safe, non-blocking in-memory transport using Python queues.
    Suitable for workers running in the same process.
    """
    def __init__(self):
        self._listeners: Dict[str, Callable[[TransportPayload], None]] = {}
        self._lock = threading.Lock()
        
        self._message_queue: queue.Queue = queue.Queue()
        self._running = True
        self._dispatcher = threading.Thread(target=self._dispatch_loop, daemon=True, name="Atlas-InMemoryTransport")
        self._dispatcher.start()

    def create_channel(self, channel_id: str) -> Result[None, TransportError]:
        # In memory, channel creation is implicit/no-op, but we validate format
        if not channel_id:
            return Result.err(TransportError("Channel ID cannot be empty"))
        return Result.ok(None)

    def send(self, channel_id: str, data: bytes) -> Result[None, TransportError]:
        """Enqueues a payload for delivery. Returns immediately."""
        with self._lock:
            if channel_id not in self._listeners:
                return Result.err(TransportError(
                    f"No listener registered on channel {channel_id}",
                    {"channel_id": channel_id}
                ))
                
        self._message_queue.put((channel_id, TransportPayload(data=data)))
        return Result.ok(None)

    def receive(self, channel_id: str, callback: Callable[[TransportPayload], None]) -> Result[None, TransportError]:
        with self._lock:
            self._listeners[channel_id] = callback
        return Result.ok(None)

    def close(self, channel_id: str) -> Result[None, TransportError]:
        with self._lock:
            if channel_id in self._listeners:
                del self._listeners[channel_id]
        return Result.ok(None)

    def _dispatch_loop(self):
        while self._running:
            try:
                channel_id, payload = self._message_queue.get(timeout=0.1)
                
                with self._lock:
                    cb = self._listeners.get(channel_id)
                
                if cb:
                    try:
                        cb(payload)
                    except Exception:
                        pass
                
                self._message_queue.task_done()
            except queue.Empty:
                continue

    def shutdown(self):
        """Cleanly shuts down the dispatcher thread."""
        self._running = False
        self._dispatcher.join(timeout=1.0)
