from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

K = TypeVar("K", bound=str)
V = TypeVar("V")


@dataclass(slots=True)
class _Entry(Generic[V]):
    value: V
    updated_at: float  # monotonic seconds


class AsyncTTLCache(Generic[K, V]):
    """
    A small async-friendly TTL cache with in-flight de-duplication.

    Notes:
    - TTL is based on monotonic time (not wall-clock).
    - `get_or_fetch()` ensures only one fetcher runs per key at a time.
    """

    def __init__(self, ttl_seconds: float):
        self._ttl = float(ttl_seconds)
        self._items: dict[K, _Entry[V]] = {}
        self._in_flight: dict[K, asyncio.Future[V]] = {}
        self._lock = asyncio.Lock()

    def _now(self) -> float:
        return time.monotonic()

    def is_fresh(self, key: K) -> bool:
        entry = self._items.get(key)
        if entry is None:
            return False
        return (self._now() - entry.updated_at) <= self._ttl

    def get(self, key: K) -> V | None:
        entry = self._items.get(key)
        if entry is None:
            return None
        if (self._now() - entry.updated_at) > self._ttl:
            return None
        return entry.value

    def set(self, key: K, value: V) -> None:
        self._items[key] = _Entry(value=value, updated_at=self._now())

    def get_or_create(self, key: K, factory: Callable[[], V]) -> V:
        """
        Identity-map helper: return existing object instance for key, otherwise create it once.

        The created entry is marked as stale until explicitly refreshed/touched.
        """
        existing = self._items.get(key)
        if existing is not None:
            return existing.value
        value = factory()
        self._items[key] = _Entry(value=value, updated_at=0.0)
        return value

    def touch(self, key: K) -> None:
        entry = self._items.get(key)
        if entry is None:
            return
        entry.updated_at = self._now()

    async def get_or_fetch(self, key: K, fetcher: Callable[[], Awaitable[V]]) -> V:
        """
        Return cached value if fresh, otherwise run `fetcher()` exactly once per key concurrently.
        """
        async with self._lock:
            cached = self.get(key)
            if cached is not None:
                return cached

            in_flight = self._in_flight.get(key)
            if in_flight is not None:
                future = in_flight
                owner = False
            else:
                loop = asyncio.get_running_loop()
                future = loop.create_future()
                self._in_flight[key] = future
                owner = True

        if owner:
            try:
                value = await fetcher()
            except Exception as e:  # noqa: BLE001
                async with self._lock:
                    if self._in_flight.get(key) is future:
                        self._in_flight.pop(key, None)
                future.set_exception(e)
                raise
            else:
                self.set(key, value)
                async with self._lock:
                    if self._in_flight.get(key) is future:
                        self._in_flight.pop(key, None)
                future.set_result(value)
                return value

        return await future
