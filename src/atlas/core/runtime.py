"""
Runtime Orchestrator for Atlas Core (Worker Architecture).

Responsible for booting, coordinating, and shutting down the Control Plane components.
"""
from atlas.core.logger import AtlasLogger
from atlas.core.configuration import ConfigurationManager
from atlas.core.lifecycle import LifecycleManager, LifecycleState
from atlas.core.registry import Registry
from atlas.core.session import SessionManager
from atlas.core.errors import BootError, ShutdownError


class AtlasRuntime:
    """
    The main orchestrator for the Atlas Control Plane.
    """

    def __init__(self):
        self.logger = AtlasLogger()
        self.config = ConfigurationManager()
        self.lifecycle = LifecycleManager(self.logger)
        self.registry = Registry(self.logger)
        self.sessions = SessionManager(self.registry, self.logger)
        
        self.state = LifecycleState.REGISTERED.value

    async def boot(self, config_path: str = "atlas.yaml") -> None:
        """
        Execute the boot sequence.
        """
        try:
            self.state = LifecycleState.INITIALIZED.value
            
            # 1. Load Configuration
            self.logger.info(f"Loading configuration from {config_path}")
            self.config.load(base_path=config_path)
            
            log_level = self.config.get("runtime.log_level", "info")
            self.logger.set_level(log_level)
            
            # 2. Initialize registered workers
            await self.lifecycle.initialize_all()
            
            # 3. Start all workers
            await self.lifecycle.start_all()
            
            self.state = LifecycleState.STARTED.value
            self.logger.info("Atlas Runtime booted successfully.")
            
        except Exception as e:
            self.state = LifecycleState.ERROR.value
            self.logger.critical(f"Boot failed: {e}")
            raise BootError("Runtime failed to boot.", reason=str(e), cause=e) from e

    async def shutdown(self) -> None:
        """
        Execute the graceful shutdown sequence.
        """
        try:
            self.logger.info("Initiating Atlas Runtime shutdown...")
            await self.lifecycle.stop_all()
            await self.lifecycle.dispose_all()
            
            self.state = LifecycleState.STOPPED.value
            self.logger.info("Atlas Runtime shutdown complete.")
            
        except Exception as e:
            self.state = LifecycleState.ERROR.value
            self.logger.error(f"Shutdown encountered errors: {e}")
            raise ShutdownError("Runtime failed during shutdown.", reason=str(e), cause=e) from e
