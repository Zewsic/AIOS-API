"""Deal entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..schemas.enums import ItemDealStatuses

if TYPE_CHECKING:  # pragma: no cover
    from ..playerok import Playerok
    from .chat import Chat
    from .user import User


@dataclass(slots=True)
class Deal:
    """Deal entity with optional client attachment."""

    id: str
    status: ItemDealStatuses | None = None
    user_id: str | None = None
    chat_id: str | None = None

    _client: Playerok | None = field(default=None, repr=False, init=False, compare=False)

    def _require_client(self) -> Playerok:
        """Ensure client is attached, raise error if not."""
        if self._client is None:
            raise RuntimeError(
                f"{self.__class__.__name__} is not attached to a client. "
                f"Use client.deals.get() to fetch an active instance."
            )
        return self._client

    async def confirm(self) -> Deal:
        """Confirm this deal."""
        return await self._require_client().deals.confirm(self.id)

    async def cancel(self) -> Deal:
        """Refund this deal."""
        return await self._require_client().deals.cancel(self.id)

    async def complete(self) -> Deal:
        """Mark deal as sent."""
        return await self._require_client().deals.complete(self.id)

    async def get_chat(self) -> Chat | None:
        """Get chat for this deal."""
        if not self.chat_id:
            return None
        return await self._require_client().chats.get(self.chat_id)

    async def get_user(self) -> User | None:
        """Get user associated with this deal."""
        if not self.user_id:
            return None
        return await self._require_client().account.get_user(self.user_id)

    async def refresh(self) -> Deal:
        """Refresh deal data from server."""
        return await self._require_client().deals.get(self.id, force_refresh=True)
