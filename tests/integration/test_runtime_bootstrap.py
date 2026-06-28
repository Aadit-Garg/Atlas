import pytest
from atlas.core.runtime import AtlasRuntime
from atlas.core.lifecycle import LifecycleState


@pytest.mark.asyncio
async def test_runtime_bootstrap_and_shutdown():
    runtime = AtlasRuntime()
    assert runtime.state == LifecycleState.REGISTERED.value
    
    await runtime.boot(config_path="nonexistent_for_test.yaml")
    
    assert runtime.state == LifecycleState.STARTED.value
    
    assert runtime.logger is not None
    assert runtime.config is not None
    assert runtime.registry is not None
    assert runtime.sessions is not None
    
    await runtime.shutdown()
    assert runtime.state == LifecycleState.STOPPED.value
