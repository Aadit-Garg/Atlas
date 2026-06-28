from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import uuid
import threading
import time

from .diagnostics import Result, RoomStateError, RoomLimitExceededError, LookupError
from .manifest import RwLock
from .session import Binding

# ---------------------------------------------------------
# Metadata & Enums
# ---------------------------------------------------------
class RoomState(Enum):
    CREATED = "Created"
    RESOLVING = "Resolving"
    ACTIVE = "Active"
    FROZEN = "Frozen"
    RECOVERING = "Recovering"
    DRAINING = "Draining"
    DESTROYED = "Destroyed"

@dataclass(frozen=True)
class RoomParticipant:
    worker_id: str
    role: str
    is_observer: bool
    joined_at: float

# ---------------------------------------------------------
# Room Registry (Local Execution Cache)
# ---------------------------------------------------------
class RoomRegistry:
    """
    Local execution cache for a specific Room.
    Workers within this Room query this registry instead of the GlobalRegistry to minimize contention.
    """
    def __init__(self):
        self._participants: Dict[str, RoomParticipant] = {}
        self._bindings: Dict[str, Binding] = {} # session_id -> Binding
        self._lock = RwLock()

    def add_participant(self, participant: RoomParticipant) -> None:
        self._lock.acquire_write()
        try:
            self._participants[participant.worker_id] = participant
        finally:
            self._lock.release_write()
            
    def remove_participant(self, worker_id: str) -> None:
        self._lock.acquire_write()
        try:
            if worker_id in self._participants:
                del self._participants[worker_id]
        finally:
            self._lock.release_write()

    def get_participant(self, worker_id: str) -> Optional[RoomParticipant]:
        self._lock.acquire_read()
        try:
            return self._participants.get(worker_id)
        finally:
            self._lock.release_read()

    def add_binding(self, binding: Binding) -> None:
        self._lock.acquire_write()
        try:
            self._bindings[binding.session_id] = binding
        finally:
            self._lock.release_write()

# ---------------------------------------------------------
# Managed Room & Steward
# ---------------------------------------------------------
class RoomSteward:
    """
    The internal coordinator for a Room.
    Enforces policies, manages the local registry, and handles observer requests.
    Does NOT execute business logic.
    """
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.registry = RoomRegistry()
        
    def handle_worker_join(self, worker_id: str, role: str, is_observer: bool) -> Result[None, Exception]:
        """Binds a worker to the room context."""
        participant = RoomParticipant(
            worker_id=worker_id,
            role=role,
            is_observer=is_observer,
            joined_at=time.time()
        )
        self.registry.add_participant(participant)
        return Result.ok(None)
        
    def handle_worker_leave(self, worker_id: str) -> None:
        self.registry.remove_participant(worker_id)


class ManagedRoom:
    """Thread-safe lifecycle manager for a Room execution context."""
    def __init__(self, room_id: str, parent_id: Optional[str] = None):
        self.room_id = room_id
        self.parent_id = parent_id
        self.state = RoomState.CREATED
        
        self.created_at = time.time()
        self.steward = RoomSteward(room_id)
        
        self._lock = threading.Lock()

    def transition(self, new_state: RoomState) -> Result[None, Exception]:
        """Strict state machine logic for Room Lifecycle."""
        with self._lock:
            # Valid transitions
            valid_moves = {
                RoomState.CREATED: [RoomState.RESOLVING, RoomState.DESTROYED],
                RoomState.RESOLVING: [RoomState.ACTIVE, RoomState.DESTROYED],
                RoomState.ACTIVE: [RoomState.FROZEN, RoomState.DRAINING, RoomState.DESTROYED],
                RoomState.FROZEN: [RoomState.RECOVERING, RoomState.DRAINING, RoomState.DESTROYED],
                RoomState.RECOVERING: [RoomState.ACTIVE, RoomState.FROZEN, RoomState.DESTROYED],
                RoomState.DRAINING: [RoomState.DESTROYED],
                RoomState.DESTROYED: []
            }
            
            if new_state not in valid_moves.get(self.state, []):
                return Result.err(RoomStateError(
                    f"Illegal room transition: {self.state.name} -> {new_state.name}"
                ))
            
            self.state = new_state
            return Result.ok(None)

# ---------------------------------------------------------
# Room Manager
# ---------------------------------------------------------
class RoomManager:
    """
    Global orchestrator for creating, tracking, and limiting Rooms.
    """
    def __init__(self, max_rooms: int = 1000, max_depth: int = 5):
        self.max_rooms = max_rooms
        self.max_depth = max_depth
        
        self._rooms: Dict[str, ManagedRoom] = {}
        self._lock = threading.Lock()

    def create_room(self, parent_id: Optional[str] = None) -> Result[str, Exception]:
        """Creates a new bounded execution context."""
        with self._lock:
            if len(self._rooms) >= self.max_rooms:
                return Result.err(RoomLimitExceededError(
                    f"Global limit of {self.max_rooms} rooms exceeded."
                ))
                
            depth = 0
            if parent_id:
                parent = self._rooms.get(parent_id)
                if not parent:
                    return Result.err(LookupError(f"Parent room {parent_id} not found"))
                
                # Calculate depth
                curr_parent: Optional[str] = parent_id
                while curr_parent:
                    depth += 1
                    node = self._rooms.get(curr_parent)
                    curr_parent = node.parent_id if node else None
                    
                if depth >= self.max_depth:
                    return Result.err(RoomLimitExceededError(
                        f"Nesting limit of {self.max_depth} exceeded."
                    ))

            room_id = str(uuid.uuid4())
            room = ManagedRoom(room_id, parent_id)
            
            # Instantly advance to Active for now (in real system, would resolve session graph first)
            room.transition(RoomState.RESOLVING).unwrap()
            room.transition(RoomState.ACTIVE).unwrap()
            
            self._rooms[room_id] = room
            return Result.ok(room_id)

    def bind_worker(self, room_id: str, worker_id: str, role: str, is_observer: bool = False) -> Result[None, Exception]:
        """Binds a worker to a Room context without duplicating it."""
        with self._lock:
            room = self._rooms.get(room_id)
            if not room: return Result.err(LookupError("Room not found"))
            
        # Cannot bind to a destroying room
        if room.state in (RoomState.DRAINING, RoomState.DESTROYED):
            return Result.err(RoomStateError("Cannot bind worker to a terminating room"))
            
        return room.steward.handle_worker_join(worker_id, role, is_observer)

    def freeze_room(self, room_id: str) -> Result[None, Exception]:
        """Pauses execution context (e.g. on critical worker failure)."""
        with self._lock:
            room = self._rooms.get(room_id)
            if not room: return Result.err(LookupError("Room not found"))
            
        return room.transition(RoomState.FROZEN)

    def recover_room(self, room_id: str) -> Result[None, Exception]:
        """Resumes execution context."""
        with self._lock:
            room = self._rooms.get(room_id)
            if not room: return Result.err(LookupError("Room not found"))
            
        res = room.transition(RoomState.RECOVERING)
        if res.is_err(): return res
        
        return room.transition(RoomState.ACTIVE)

    def destroy_room(self, room_id: str) -> Result[None, Exception]:
        with self._lock:
            room = self._rooms.get(room_id)
            if not room: return Result.err(LookupError("Room not found"))
            
            room.transition(RoomState.DRAINING).unwrap()
            room.transition(RoomState.DESTROYED).unwrap()
            
            del self._rooms[room_id]
            return Result.ok(None)
