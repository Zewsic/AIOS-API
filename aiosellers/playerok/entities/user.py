from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..schemas.account import UserProfile as SchemaUserProfile
from ..schemas.enums import UserType

if TYPE_CHECKING:  # pragma: no cover
    from ..playerok import Playerok


@dataclass(slots=True)
class User:
    id: str
    username: str | None = None
    avatar_url: str | None = None
    role: UserType = UserType.USER
    is_online: bool | None = None
    is_blocked: bool | None = None
    rating: float | None = None
    reviews_count: int | None = None

    _client: "Playerok" = field(repr=False, default=None)

    @classmethod
    def _create(cls, *, client: "Playerok", id: str) -> "User":
        return cls(id=id, _client=client)

    def _merge_profile(self, profile: SchemaUserProfile) -> None:
        self.username = profile.username
        self.avatar_url = profile.avatar_url
        self.role = profile.role
        self.is_online = profile.is_online
        self.is_blocked = profile.is_blocked
        self.rating = profile.rating
        self.reviews_count = profile.reviews_count

    async def refresh(self) -> "User":
        await self._client._push_user(self.id)
        return self
