"""Chat entity and related classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from ..schemas import ChatTypes

if TYPE_CHECKING:  # pragma: no cover
    from ..playerok import Playerok
    from .deal import Deal
    from .file import File
    from .user import User


@dataclass(slots=True)
class ChatMessage:
    """Chat message entity."""

    id: str
    sent_at: datetime
    is_read: bool
    text: str | None = None
    file: File | None = None
    user_id: str | None = None
    chat_id: str | None = None


@dataclass(slots=True)
class Chat:
    """Chat entity with optional client attachment."""

    id: str
    type: ChatTypes = ChatTypes.PM
    unread_messages_counter: int | None = None
    user_id: str | None = None

    _client: Playerok | None = field(default=None, repr=False, init=False, compare=False)

    def _require_client(self) -> Playerok:
        """Ensure client is attached, raise error if not."""
        if self._client is None:
            raise RuntimeError(
                f"{self.__class__.__name__} is not attached to a client. "
                f"Use client.chats.get() to fetch an active instance."
            )
        return self._client

    async def send_text(self, text: str, *, mark_as_read: bool = False) -> ChatMessage:
        """Send text message to this chat."""
        return await self._require_client().chats.send_message(
            self.id, text=text, mark_as_read=mark_as_read
        )

    async def send_photo(self, path: str | Path, *, mark_as_read: bool = False) -> ChatMessage:
        """Send photo to this chat."""
        return await self._require_client().chats.send_message(
            self.id, photo=path, mark_as_read=mark_as_read
        )

    async def mark_as_read(self) -> None:
        """Mark this chat as read."""
        await self._require_client().chats.mark_as_read(self.id)

    async def get_messages(self, limit: int = 50) -> list[ChatMessage]:
        """Get messages from this chat."""
        return await self._require_client().chats.messages.list(self.id, limit=limit)

    async def get_user(self) -> User | None:
        """Get the other participant in this chat."""
        if not self.user_id:
            return None
        return await self._require_client().account.get_user(self.user_id)

    async def get_deals(self) -> list[Deal]:
        """Get all deals associated with this chat."""
        from .deal import Deal

        client = self._require_client()
        # Refresh chat schema to get deals
        schema = await client._raw.chats.get_chat(self.id)
        if schema is None or not schema.deals:
            return []

        # Convert schema deals to Deal entities
        deals = []
        for deal_schema in schema.deals:
            deal = Deal(
                id=deal_schema.id,
                status=deal_schema.status,
                user_id=deal_schema.user.id if deal_schema.user else None,
                chat_id=self.id,
            )
            deal._client = client
            if client._use_identity_map:
                client._identity_maps.deals.set(deal_schema.id, deal)
            deals.append(deal)

        return deals

    async def refresh(self) -> Chat:
        """Refresh chat data from server."""
        return await self._require_client().chats.get(self.id, force_refresh=True)
