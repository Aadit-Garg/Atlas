"""
Error hierarchy for Atlas Core (Worker Architecture).

All Atlas errors inherit from `AtlasError` and must contain:
- message: Human-readable description
- reason: Why the error occurred
- context: Relevant state at the time of failure
- resolution: Suggested fix or next step
"""
from typing import Any


class AtlasError(Exception):
    """Base class for all Atlas errors."""

    def __init__(
        self,
        message: str,
        reason: str,
        context: dict[str, Any] | None = None,
        resolution: str = "",
        cause: Exception | None = None,
        error_code: str | None = None,
    ):
        self.message = message
        self.reason = reason
        self.context = context or {}
        self.resolution = resolution
        self.cause = cause
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self) -> str:
        base = f"[{self.__class__.__name__}] {self.message}\nReason: {self.reason}"
        if self.context:
            base += f"\nContext: {self.context}"
        if self.resolution:
            base += f"\nResolution: {self.resolution}"
        if self.error_code:
            base += f"\nError Code: {self.error_code}"
        return base


class ConfigurationError(AtlasError): pass
class ConfigNotFoundError(ConfigurationError): pass
class ConfigValidationError(ConfigurationError): pass

class LifecycleError(AtlasError): pass
class InvalidTransitionError(LifecycleError): pass
class InitializationError(LifecycleError): pass
class ShutdownError(LifecycleError): pass

class RegistryError(AtlasError): pass
class DuplicateRegistrationError(RegistryError): pass
class ComponentNotFoundError(RegistryError): pass
class IncompatibleVersionError(RegistryError): pass

class SessionError(AtlasError): pass
class CapabilityNotFoundError(SessionError): pass
class WorkerNotAvailableError(SessionError): pass
class PermissionDeniedError(SessionError): pass

class WorkerError(AtlasError): pass
class WorkerLoadError(WorkerError): pass
class WorkerManifestError(WorkerError): pass

class RuntimeError(AtlasError): pass
class BootError(RuntimeError): pass
