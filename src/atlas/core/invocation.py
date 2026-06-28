from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import uuid
import threading
import time

from .diagnostics import Result, InvocationStateError, LookupError
from .manifest import RwLock

# ---------------------------------------------------------
# Metadata & Enums
# ---------------------------------------------------------
class InvocationState(Enum):
    CREATED = "Created"
    QUEUED = "Queued"
    DISPATCHED = "Dispatched"
    EXECUTING = "Executing"
    WAITING = "Waiting"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    TIMED_OUT = "TimedOut"
    FAILED = "Failed"

class RetryPolicy(Enum):
    NEVER = "Never"
    IMMEDIATE = "Immediate"
    DELAYED = "Delayed"
    EXPONENTIAL = "Exponential"
    CUSTOM = "Custom"

@dataclass(frozen=True)
class InvocationResult:
    status: InvocationState
    data: Optional[Any] = None
    error: Optional[str] = None
    diagnostics: Dict[str, str] = field(default_factory=dict)

@dataclass(frozen=True)
class InvocationContext:
    """Immutable execution context carried through the Invocation lifecycle."""
    invocation_id: str
    session_id: str
    worker_id: str
    parent_id: Optional[str]
    root_id: str
    correlation_id: str
    retry_policy: RetryPolicy = RetryPolicy.NEVER
    timeout_ms: Optional[int] = None
    metadata: Dict[str, str] = field(default_factory=dict)

# ---------------------------------------------------------
# Managed Invocation (State Machine)
# ---------------------------------------------------------
class ManagedInvocation:
    """Thread-safe lifecycle manager for an Invocation."""
    def __init__(self, context: InvocationContext):
        self.context = context
        self.state = InvocationState.CREATED
        
        self.created_at = time.time()
        self.completed_at: Optional[float] = None
        self.result: Optional[InvocationResult] = None
        
        # Used for cooperative cancellation. If True, the worker is expected to gracefully exit.
        self.cancellation_requested = False
        
        self._lock = threading.Lock()

    def transition(self, new_state: InvocationState) -> Result[None, Exception]:
        """Strict state machine logic for Invocation Lifecycle."""
        with self._lock:
            if self._is_terminal(self.state):
                return Result.err(InvocationStateError(
                    f"Cannot transition from terminal state {self.state.name} to {new_state.name}"
                ))

            # Valid transitions
            valid_moves = {
                InvocationState.CREATED: [InvocationState.QUEUED, InvocationState.CANCELLED],
                InvocationState.QUEUED: [InvocationState.DISPATCHED, InvocationState.CANCELLED, InvocationState.TIMED_OUT],
                InvocationState.DISPATCHED: [InvocationState.EXECUTING, InvocationState.CANCELLED, InvocationState.TIMED_OUT, InvocationState.FAILED],
                InvocationState.EXECUTING: [InvocationState.WAITING, InvocationState.COMPLETED, InvocationState.CANCELLED, InvocationState.TIMED_OUT, InvocationState.FAILED],
                InvocationState.WAITING: [InvocationState.EXECUTING, InvocationState.COMPLETED, InvocationState.CANCELLED, InvocationState.TIMED_OUT, InvocationState.FAILED],
            }
            
            if new_state not in valid_moves.get(self.state, []):
                return Result.err(InvocationStateError(
                    f"Illegal invocation transition: {self.state.name} -> {new_state.name}"
                ))
            
            self.state = new_state
            if self._is_terminal(new_state):
                self.completed_at = time.time()
                
            return Result.ok(None)

    def _is_terminal(self, state: InvocationState) -> bool:
        return state in (InvocationState.COMPLETED, InvocationState.CANCELLED, 
                         InvocationState.TIMED_OUT, InvocationState.FAILED)

    def request_cancellation(self) -> None:
        """Flags the invocation for cancellation (Cooperative)."""
        with self._lock:
            if not self._is_terminal(self.state):
                self.cancellation_requested = True

# ---------------------------------------------------------
# Invocation Registry
# ---------------------------------------------------------
class InvocationRegistry:
    """In-memory index of all invocations, facilitating O(1) trace reconstruction."""
    def __init__(self):
        self._active_invocations: Dict[str, ManagedInvocation] = {}
        self._completed_invocations: Dict[str, ManagedInvocation] = {}
        
        # parent_id -> List[child_ids]
        self._children_index: Dict[str, List[str]] = {}
        self._lock = RwLock()

    def register(self, invocation: ManagedInvocation) -> None:
        self._lock.acquire_write()
        try:
            inv_id = invocation.context.invocation_id
            self._active_invocations[inv_id] = invocation
            
            parent_id = invocation.context.parent_id
            if parent_id:
                if parent_id not in self._children_index:
                    self._children_index[parent_id] = []
                self._children_index[parent_id].append(inv_id)
        finally:
            self._lock.release_write()

    def mark_terminal(self, invocation_id: str) -> None:
        self._lock.acquire_write()
        try:
            if invocation_id in self._active_invocations:
                inv = self._active_invocations.pop(invocation_id)
                self._completed_invocations[invocation_id] = inv
        finally:
            self._lock.release_write()

    def get(self, invocation_id: str) -> Optional[ManagedInvocation]:
        self._lock.acquire_read()
        try:
            return self._active_invocations.get(invocation_id) or self._completed_invocations.get(invocation_id)
        finally:
            self._lock.release_read()

    def get_children(self, parent_id: str) -> List[str]:
        self._lock.acquire_read()
        try:
            return list(self._children_index.get(parent_id, []))
        finally:
            self._lock.release_read()

# ---------------------------------------------------------
# Invocation Engine
# ---------------------------------------------------------
class InvocationEngine:
    """
    Manages the creation, traceability, and cancellation of work.
    Does not schedule or execute work directly.
    """
    def __init__(self):
        self.registry = InvocationRegistry()

    def create_invocation(
        self, session_id: str, worker_id: str, 
        parent_id: Optional[str] = None, 
        correlation_id: Optional[str] = None,
        retry_policy: RetryPolicy = RetryPolicy.NEVER,
        timeout_ms: Optional[int] = None
    ) -> Result[ManagedInvocation, Exception]:
        """Creates a new Invocation, calculating proper Root IDs based on parent context."""
        inv_id = str(uuid.uuid4())
        
        if parent_id:
            parent_inv = self.registry.get(parent_id)
            if not parent_inv:
                return Result.err(LookupError(f"Parent invocation {parent_id} not found"))
            
            root_id = parent_inv.context.root_id
            corr_id = parent_inv.context.correlation_id
        else:
            root_id = inv_id
            corr_id = correlation_id or str(uuid.uuid4())
            
        context = InvocationContext(
            invocation_id=inv_id,
            session_id=session_id,
            worker_id=worker_id,
            parent_id=parent_id,
            root_id=root_id,
            correlation_id=corr_id,
            retry_policy=retry_policy,
            timeout_ms=timeout_ms
        )
        
        inv = ManagedInvocation(context)
        self.registry.register(inv)
        return Result.ok(inv)

    def complete(self, invocation_id: str, result_data: Any = None) -> Result[None, Exception]:
        inv = self.registry.get(invocation_id)
        if not inv: return Result.err(LookupError("Invocation not found"))
        
        res = inv.transition(InvocationState.COMPLETED)
        if res.is_err(): return res
        
        inv.result = InvocationResult(status=InvocationState.COMPLETED, data=result_data)
        self.registry.mark_terminal(invocation_id)
        return Result.ok(None)
        
    def fail(self, invocation_id: str, error: str) -> Result[None, Exception]:
        inv = self.registry.get(invocation_id)
        if not inv: return Result.err(LookupError("Invocation not found"))
        
        res = inv.transition(InvocationState.FAILED)
        if res.is_err(): return res
        
        inv.result = InvocationResult(status=InvocationState.FAILED, error=error)
        self.registry.mark_terminal(invocation_id)
        return Result.ok(None)

    def cancel(self, invocation_id: str) -> Result[None, Exception]:
        """
        Cooperative cancellation. Flags the target invocation and all of its descendants recursively.
        """
        inv = self.registry.get(invocation_id)
        if not inv: return Result.err(LookupError("Invocation not found"))
        
        inv.request_cancellation()
        
        # Attempt immediate transition if it's currently active (Worker might still be executing though)
        # In a real system, the Worker polls `cancellation_requested` and transitions itself to CANCELLED.
        # For tracking, we forcefully flag the cascade.
        inv.transition(InvocationState.CANCELLED)
        if inv._is_terminal(inv.state):
            inv.result = InvocationResult(status=InvocationState.CANCELLED, error="Cancelled by user/system")
            self.registry.mark_terminal(invocation_id)
            
        # Recursive cascade
        children = self.registry.get_children(invocation_id)
        for child_id in children:
            self.cancel(child_id)
            
        return Result.ok(None)

    def trace(self, invocation_id: str) -> Result[List[str], Exception]:
        """Reconstructs the path from Root to the given invocation."""
        path = []
        current_id: Optional[str] = invocation_id
        
        while current_id:
            path.append(current_id)
            inv = self.registry.get(current_id)
            if not inv:
                return Result.err(LookupError(f"Broken trace: Invocation {current_id} not found"))
            current_id = inv.context.parent_id
            
        path.reverse()
        return Result.ok(path)
