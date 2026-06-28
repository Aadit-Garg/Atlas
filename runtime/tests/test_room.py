import pytest

from atlas.core.room import RoomManager, RoomState
from atlas.core.diagnostics import RoomStateError, RoomLimitExceededError

@pytest.fixture
def manager():
    return RoomManager(max_rooms=100, max_depth=3)

def test_room_lifecycle(manager):
    room_id = manager.create_room().unwrap()
    room = manager._rooms[room_id]
    
    assert room.state == RoomState.ACTIVE
    
    manager.freeze_room(room_id).unwrap()
    assert room.state == RoomState.FROZEN
    
    manager.recover_room(room_id).unwrap()
    assert room.state == RoomState.ACTIVE
    
    manager.destroy_room(room_id).unwrap()
    assert room_id not in manager._rooms

def test_shared_workers(manager):
    # Worker A joins Room 1 and Room 2
    r1 = manager.create_room().unwrap()
    r2 = manager.create_room().unwrap()
    
    manager.bind_worker(r1, "WorkerA", "UI").unwrap()
    manager.bind_worker(r2, "WorkerA", "UI").unwrap()
    
    # Verify Worker A exists in both room registries without conflict
    assert manager._rooms[r1].steward.registry.get_participant("WorkerA") is not None
    assert manager._rooms[r2].steward.registry.get_participant("WorkerA") is not None

def test_nested_limits(manager):
    r1 = manager.create_room().unwrap() # Depth 0
    r2 = manager.create_room(parent_id=r1).unwrap() # Depth 1
    r3 = manager.create_room(parent_id=r2).unwrap() # Depth 2
    
    # Exceeding Depth 3 limit
    res = manager.create_room(parent_id=r3)
    assert res.is_err()
    assert isinstance(res.error, RoomLimitExceededError)

def test_observer_bindings(manager):
    room_id = manager.create_room().unwrap()
    
    # Miron binds as Observer
    manager.bind_worker(room_id, "MironTracker", "profiler", is_observer=True).unwrap()
    
    part = manager._rooms[room_id].steward.registry.get_participant("MironTracker")
    assert part is not None
    assert part.is_observer is True
    
def test_illegal_lifecycle_transitions(manager):
    room_id = manager.create_room().unwrap()
    room = manager._rooms[room_id]
    
    # Cannot jump from ACTIVE to RECOVERING (must freeze first)
    res = room.transition(RoomState.RECOVERING)
    assert res.is_err()
    assert isinstance(res.error, RoomStateError)
