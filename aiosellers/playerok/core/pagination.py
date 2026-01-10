"""Generic pagination helper (currently unused - inlined in API modules for simplicity)."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def paginate(
    fetcher: Callable[[int, str | None], Awaitable[tuple[list[T], str | None, bool]]],
    limit: int,
) -> list[T]:
    """Generic pagination helper.

    Args:
        fetcher: Async function that takes (count, cursor) and returns (items, next_cursor, has_more).
        limit: Maximum number of items to fetch.

    Returns:
        List of items up to limit.

    Note:
        This is a generic helper that can be used for any paginated API.
        Currently each API module implements pagination inline for clarity.
    """
    result = []
    remain = limit
    cursor = None

    while remain > 0:
        items, next_cursor, has_more = await fetcher(min(24, remain), cursor)
        result.extend(items[:remain])
        remain -= len(items)

        if not has_more or not next_cursor:
            break
        cursor = next_cursor

    return result
