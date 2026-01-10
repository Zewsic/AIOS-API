from __future__ import annotations

from collections.abc import Iterable
from io import BytesIO
from pathlib import Path
from typing import Any

from .exceptions import GraphQLError
from .types import ImageInput


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


async def prepare_image_file(image: ImageInput) -> tuple[Any, bool]:
    from tls_requests import AsyncClient

    if isinstance(image, BytesIO):
        return image, False

    if isinstance(image, bytes):
        return BytesIO(image), False

    if isinstance(image, Path):
        image = str(image)

    if isinstance(image, str):
        if image.startswith(("http://", "https://")):
            async with AsyncClient() as client:
                response = await client.get(image)
                if hasattr(response, "status_code") and response.status_code >= 400:
                    raise RuntimeError(
                        f"Failed to download image from {image}: HTTP {response.status_code}"
                    )
                content = getattr(response, "content", None)
                if content is None:
                    content = getattr(response, "text", "").encode()
                return BytesIO(content), False
        else:
            file_obj = open(image, "rb")
            return file_obj, True

    raise TypeError(f"Unsupported image type: {type(image)}")
