from collections.abc import Iterable
from typing import Any

from .exceptions import GraphQLError


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
        if len(errors) >= 1:
            if "message" in errors[0]:
                raise GraphQLError(errors[0]["message"] + ": " + str(errors[0]))
            raise GraphQLError(errors[0])
        raise GraphQLError(errors)
