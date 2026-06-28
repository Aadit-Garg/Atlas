import logging
from typing import Optional, Dict, Any

from .model import LoggerModel

class ConsoleLoggerWorker(LoggerModel):
    """
    Reference Implementation of the LoggerModel.
    Provides standard python logging capabilities.
    """
    def __init__(self):
        self.logger = logging.getLogger("atlas.stdlib.logger")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def _format_context(self, message: str, context: Optional[Dict[str, Any]]) -> str:
        if context:
            return f"{message} | ctx: {context}"
        return message

    def debug(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        self.logger.debug(self._format_context(message, context))

    def info(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        self.logger.info(self._format_context(message, context))

    def warn(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        self.logger.warning(self._format_context(message, context))

    def error(self, message: str, exc_info: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> None:
        msg = self._format_context(message, context)
        if exc_info:
            msg = f"{msg} | Ex: {exc_info}"
        self.logger.error(msg)
