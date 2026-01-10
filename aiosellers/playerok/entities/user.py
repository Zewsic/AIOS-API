from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..schemas.enums import UserType

if TYPE_CHECKING:  # pragma: no cover
    from ..playerok import Playerok
    from ..schemas import UserProfile
    from .chat import Chat
    from .deal import Deal


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

    _client: Playerok | None = field(default=None, repr=False, init=False, compare=False)

    @staticmethod
    def from_schema(schema: UserProfile, client: Playerok) -> User:
        user = User(
            id=schema.id,
            username=schema.username,
            avatar_url=schema.avatar_url,
            role=schema.role,
            is_online=schema.is_online,
            is_blocked=schema.is_blocked,
            rating=schema.rating,
            reviews_count=schema.reviews_count,
        )
        user._client = client
        return user

    def _require_client(self) -> Playerok:
        if self._client is None:
            raise RuntimeError(
                f"{self.__class__.__name__} is not attached to a client. "
                f"Use client.account.get_user() to fetch an active instance."
            )
        return self._client

    async def refresh(self) -> User:
        return await self._require_client().account.get_user(self.id, force_refresh=True)

    async def get_chat(self) -> Chat | None:
        chats = await self._require_client().chats.list(user_id=self.id, limit=1)
        return chats[0] if chats else None

    async def get_deals(self, limit: int = 24) -> list[Deal]:
        return await self._require_client().deals.list(user_id=self.id, limit=limit)
