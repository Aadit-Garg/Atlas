import time
from datetime import datetime, timezone

from .model import ClockModel

class SystemClockWorker(ClockModel):
    """
    Reference Implementation of the ClockModel.
    Provides standard system time access.
    """
    def now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def timestamp(self) -> float:
        return time.time()

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)
