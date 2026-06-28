"""
Atlas Room Manager Demonstration
Demonstrates nested limits, observer session binding, and the freeze/recovery lifecycle.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from atlas.core.room import RoomManager, RoomState

def run_demo():
    print("Initializing Atlas Room Manager (Limits: Max Depth 3)...")
    manager = RoomManager(max_depth=3)
    
    print("\n[Scenario 1] Nested Limits Enforcement")
    
    print("  -> Creating Root Room (Depth 0)")
    r1 = manager.create_room().unwrap()
    print("  -> Creating Sub-Room (Depth 1)")
    r2 = manager.create_room(parent_id=r1).unwrap()
    print("  -> Creating Sub-Room (Depth 2)")
    r3 = manager.create_room(parent_id=r2).unwrap()
    
    print("  -> Attempting to create Sub-Room (Depth 3) - Expecting Rejection:")
    res = manager.create_room(parent_id=r3)
    if res.is_err():
        print(f"     [Rejected] {res.error.message}")
        
    print("\n[Scenario 2] Worker Sharing & Observers")
    print(f"  -> Binding 'PythonWorkerA' to Room {r1[:8]}")
    manager.bind_worker(r1, "PythonWorkerA", "App").unwrap()
    
    print(f"  -> Binding 'PythonWorkerA' to Room {r2[:8]} (Sharing worker across boundaries)")
    manager.bind_worker(r2, "PythonWorkerA", "App").unwrap()
    
    print(f"  -> Binding 'MironTelemetry' as Observer to Room {r1[:8]}")
    manager.bind_worker(r1, "MironTelemetry", "Profiler", is_observer=True).unwrap()
    
    r1_steward = manager._rooms[r1].steward
    print("  -> Room 1 Participants:")
    for p in r1_steward.registry._participants.values():
        print(f"     - {p.worker_id} (Role: {p.role}, Observer: {p.is_observer})")
        
    print("\n[Scenario 3] Freeze & Recovery")
    print("  -> Simulating critical Worker failure in Room 1...")
    manager.freeze_room(r1).unwrap()
    state = manager._rooms[r1].state
    print(f"  -> Room 1 State: {state.value} (Outstanding Invocations Paused)")
    
    print("  -> Simulating Miron Recovery Hook executing...")
    manager.recover_room(r1).unwrap()
    state = manager._rooms[r1].state
    print(f"  -> Room 1 State: {state.value} (Invocations Resumed)")
    
    print("\n[Scenario 4] Destruction")
    manager.destroy_room(r1).unwrap()
    manager.destroy_room(r2).unwrap()
    manager.destroy_room(r3).unwrap()
    print("All rooms cleanly drained and destroyed.")

if __name__ == "__main__":
    run_demo()
