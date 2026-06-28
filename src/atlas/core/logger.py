"""
Structured logging implementation for Atlas Core.
"""
import logging
from typing import Any, Protocol


class LoggerProtocol(Protocol):
    def debug(self, message: str, **context: Any) -> None: ...
    def info(self, message: str, **context: Any) -> None: ...
    def warning(self, message: str, **context: Any) -> None: ...
    def error(self, message: str, **context: Any) -> None: ...
    def critical(self, message: str, **context: Any) -> None: ...
    def child(self, name: str) -> "LoggerProtocol": ...


class AtlasLogger:
    """
    Default structured logger implementation wrapping the standard library logger.
    """

    def __init__(self, name: str = "atlas", level: int = logging.INFO):
        self._name = name
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            self._logger.setLevel(level)
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def _format_message(self, message: str, context: dict[str, Any]) -> str:
        if not context:
            return message
        context_str = " ".join(f"{k}={v}" for k, v in context.items())
        return f"{message} | {context_str}"

    def debug(self, message: str, **context: Any) -> None:
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(self._format_message(message, context))

    def info(self, message: str, **context: Any) -> None:
        if self._logger.isEnabledFor(logging.INFO):
            self._logger.info(self._format_message(message, context))

    def warning(self, message: str, **context: Any) -> None:
        if self._logger.isEnabledFor(logging.WARNING):
            self._logger.warning(self._format_message(message, context))

    def error(self, message: str, **context: Any) -> None:
        if self._logger.isEnabledFor(logging.ERROR):
            self._logger.error(self._format_message(message, context))

    def critical(self, message: str, **context: Any) -> None:
        if self._logger.isEnabledFor(logging.CRITICAL):
            self._logger.critical(self._format_message(message, context))

    def child(self, name: str) -> "AtlasLogger":
        return AtlasLogger(name=f"{self._name}.{name}", level=self._logger.level)

    def set_level(self, level: int | str) -> None:
        if isinstance(level, str):
            level = logging.getLevelNamesMapping().get(level.upper(), logging.INFO)
        self._logger.setLevel(level)
