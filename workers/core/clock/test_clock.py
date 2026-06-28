import pytest
import time
from workers.core.clock.worker import SystemClockWorker

def test_system_clock_implements_model():
    clock = SystemClockWorker()
    
    # Test now() ISO format
    now_str = clock.now()
    assert "T" in now_str
    assert "+00:00" in now_str
    
    # Test timestamp
    ts1 = clock.timestamp()
    assert isinstance(ts1, float)
    
    # Test sleep
    clock.sleep(0.1)
    ts2 = clock.timestamp()
    
    assert ts2 > ts1
    assert (ts2 - ts1) >= 0.1
