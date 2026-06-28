"""
Atlas Invocation Engine Demonstration
Demonstrates nested parent/child execution tracking and cooperative cancellation cascades.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from atlas.core.invocation import InvocationEngine, InvocationState

def run_demo():
    print("Initializing Atlas Invocation Engine...")
    engine = InvocationEngine()
    
    print("\n[Scenario 1] Nested Invocation Tracing")
    
    # 1. A User Request enters the system (Root)
    print("  -> Creating Root Invocation A (Worker A)")
    invA = engine.create_invocation("sess-1", "WorkerA").unwrap()
    id_a = invA.context.invocation_id
    
    # 2. Worker A calls Worker B
    print("  -> Worker A calls Worker B (Child Invocation B)")
    invB = engine.create_invocation("sess-2", "WorkerB", parent_id=id_a).unwrap()
    id_b = invB.context.invocation_id
    
    # 3. Worker B calls Worker C
    print("  -> Worker B calls Worker C (Child Invocation C)")
    invC = engine.create_invocation("sess-3", "WorkerC", parent_id=id_b).unwrap()
    id_c = invC.context.invocation_id
    
    print("\n[Tracing Execution Path]")
    trace = engine.trace(id_c).unwrap()
    for depth, t_id in enumerate(trace):
        print(f"  Level {depth}: {t_id}")
        
    print("\n[Scenario 2] Cooperative Cancellation Cascade")
    print("  -> User cancels the original request (Root A)")
    engine.cancel(id_a)
    
    print("\n[Inspecting State Machine]")
    for inv_id in [id_a, id_b, id_c]:
        state = engine.registry.get(inv_id).state
        print(f"  Invocation {inv_id} State: {state.value}")
        
    print("\nNotice how cancelling the Root instantly cascaded and cancelled all descendants!")

if __name__ == "__main__":
    run_demo()
