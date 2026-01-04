from collections.abc import Iterable
from typing import Any


def _dig(obj: dict[str, Any], path: Iterable[str]) -> Any:
    cur: Any = obj
    for key in path:
        if cur is None:
            return None
        cur = cur.get(key)
    return cur


def _raise_on_gql_errors(payload: dict[str, Any]) -> None:
    errors = payload.get("errors")
    if errors:
        raise RuntimeError(f"GraphQL errors: {errors}")
