"""
Atlas Transport Layer Demonstration
This script proves the successful implementation of the Transport Layer.
It spins up two mock components and pushes bytes between them using the InMemoryTransport.
"""
import time
import sys
import os

# Add src to path so we can run this directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from atlas.core.transport import InMemoryTransport, TransportPayload

def run_demo():
    print("Initializing Atlas InMemoryTransport...")
    transport = InMemoryTransport()
    transport.create_channel("demo-channel").unwrap()
    
    received = False
    
    # 1. Register the Target Listener (Mock Worker B)
    def on_receive(payload: TransportPayload):
        nonlocal received
        print(f"\n[Worker B] Received payload!")
        print(f"[Worker B] Raw bytes: {payload.data}")
        print(f"[Worker B] Decoded text: {payload.data.decode('utf-8')}")
        received = True
        
    print("Registering listener on 'demo-channel'...")
    transport.receive("demo-channel", on_receive)
    
    # 2. Send bytes from Source (Mock Worker A)
    print("\n[Worker A] Preparing to send raw bytes...")
    message = "Hello from the Transport Layer!".encode("utf-8")
    
    res = transport.send("demo-channel", message)
    if res.is_ok():
        print("[Worker A] Payload sent successfully into the transport queue.")
    else:
        print(f"[Worker A] Failed to send: {res.error}")
        
    # Wait for async delivery
    time.sleep(0.5)
    
    if received:
        print("\nDemonstration successful! The Transport Layer correctly moved bytes asynchronously.")
    
    transport.shutdown()

if __name__ == "__main__":
    run_demo()
