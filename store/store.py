from __future__ import annotations

import random
import time
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class Store:

    def __init__(self, timeout: float = 0.5, max_retries: int = 3) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self._data: dict[str, Any] = {}


    def _call_with_retry(self, func: callable, *args: Any, **kwargs: Any) -> Any:
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                last_exc = exc
                logger.warning(
                    "Store operation failed (attempt %d/%d): %s",
                    attempt,
                    self.max_retries,
                    exc,
                )
                if attempt == self.max_retries:
                    break

                delay = (2 ** (attempt - 1)) * 0.1 + random.random() * 0.1
                time.sleep(delay)
        if last_exc is not None:
            raise last_exc


    def set(self, key: str, value: Any) -> bool:
        def _inner():
            time.sleep(random.uniform(0, self.timeout))
            if random.random() < 0.2:  # 20% шанс ошибки
                raise IOError("Simulated network error")
            self._data[key] = value
            return True

        return self._call_with_retry(_inner)


    def get(self, key: str) -> Optional[Any]:
        def _inner():
            time.sleep(random.uniform(0, self.timeout))
            if random.random() < 0.2:
                raise IOError("Simulated network error")
            return self._data.get(key)

        return self._call_with_retry(_inner)


    def cache_set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        return self.set(key, value)


    def cache_get(self, key: str) -> Optional[Any]:
        return self.get(key)
