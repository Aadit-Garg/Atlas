import pytest
import threading

from atlas.core.invocation import InvocationEngine, InvocationState, RetryPolicy
from atlas.core.diagnostics import InvocationStateError

@pytest.fixture
def engine():
    return InvocationEngine()

def test_invocation_lifecycle(engine):
    # Created -> Queued -> Dispatched -> Executing -> Waiting -> Executing -> Completed
    inv = engine.create_invocation("sess-1", "workerA").unwrap()
    inv_id = inv.context.invocation_id
    
    assert inv.state == InvocationState.CREATED
    assert inv.transition(InvocationState.QUEUED).is_ok()
    assert inv.transition(InvocationState.DISPATCHED).is_ok()
    assert inv.transition(InvocationState.EXECUTING).is_ok()
    assert inv.transition(InvocationState.WAITING).is_ok()
    assert inv.transition(InvocationState.EXECUTING).is_ok()
    
    res = engine.complete(inv_id, result_data={"status": "success"})
    assert res.is_ok()
    
    # Verify Registry marked terminal
    fetched = engine.registry.get(inv_id)
    assert fetched.state == InvocationState.COMPLETED
    assert fetched.result.data == {"status": "success"}

def test_illegal_lifecycle_transitions(engine):
    inv = engine.create_invocation("sess-1", "workerA").unwrap()
    inv.transition(InvocationState.QUEUED).unwrap()
    
    # Cannot jump from QUEUED to COMPLETED
    res = inv.transition(InvocationState.COMPLETED)
    assert res.is_err()
    assert isinstance(res.error, InvocationStateError)

def test_parent_child_tracing(engine):
    # A -> B -> C
    invA = engine.create_invocation("sess-1", "workerA").unwrap()
    invB = engine.create_invocation("sess-2", "workerB", parent_id=invA.context.invocation_id).unwrap()
    invC = engine.create_invocation("sess-3", "workerC", parent_id=invB.context.invocation_id).unwrap()
    
    # All share the same root and correlation ID
    assert invC.context.root_id == invA.context.invocation_id
    assert invC.context.correlation_id == invA.context.correlation_id
    
    trace = engine.trace(invC.context.invocation_id).unwrap()
    assert len(trace) == 3
    assert trace[0] == invA.context.invocation_id
    assert trace[1] == invB.context.invocation_id
    assert trace[2] == invC.context.invocation_id

def test_recursive_cancellation(engine):
    # A -> B -> C
    invA = engine.create_invocation("sess-1", "workerA").unwrap()
    invB = engine.create_invocation("sess-2", "workerB", parent_id=invA.context.invocation_id).unwrap()
    invC = engine.create_invocation("sess-3", "workerC", parent_id=invB.context.invocation_id).unwrap()
    
    # Cancel root
    engine.cancel(invA.context.invocation_id).unwrap()
    
    assert invA.cancellation_requested is True
    assert invB.cancellation_requested is True
    assert invC.cancellation_requested is True
    
    assert invA.state == InvocationState.CANCELLED
    assert invC.state == InvocationState.CANCELLED

def test_concurrent_invocations(engine):
    def spawn_batch():
        for _ in range(100):
            engine.create_invocation("sess", "worker")
            
    threads = [threading.Thread(target=spawn_batch) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    # 10 threads * 100 invocations
    assert len(engine.registry._active_invocations) == 1000
