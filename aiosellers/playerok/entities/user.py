"""User entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..schemas.enums import UserType

if TYPE_CHECKING:  # pragma: no cover
    from ..playerok import Playerok


@dataclass(slots=True)
class User:
    """User entity with optional client attachment."""

    id: str
    username: str | None = None
    avatar_url: str | None = None
    role: UserType = UserType.USER
    is_online: bool | None = None
    is_blocked: bool | None = None
    rating: float | None = None
    reviews_count: int | None = None

    _client: Playerok | None = field(default=None, repr=False, init=False, compare=False)

    def _require_client(self) -> Playerok:
        """Ensure client is attached, raise error if not."""
        if self._client is None:
            raise RuntimeError(
                f"{self.__class__.__name__} is not attached to a client. "
                f"Use client.account.get_user() to fetch an active instance."
            )
        return self._client

    async def refresh(self) -> User:
        """Refresh user data from server."""
        return await self._require_client().account.get_user(self.id, force_refresh=True)
