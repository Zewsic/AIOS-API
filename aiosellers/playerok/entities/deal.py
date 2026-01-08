from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..schemas.deals import ItemDeal as SchemaDeal
from ..schemas.enums import ItemDealStatuses

if TYPE_CHECKING:  # pragma: no cover
    from ..playerok import Playerok
    from .chat import Chat
    from .user import User


@dataclass(slots=True)
class Deal:
    id: str
    status: ItemDealStatuses | None = None

    _client: "Playerok" = field(repr=False, default=None)
    _user_id: str | None = field(repr=False, default=None)
    _chat_id: str | None = field(repr=False, default=None)

    @classmethod
    def _create(cls, *, client: "Playerok", id: str) -> "Deal":
        return cls(id=id, _client=client)

    def _merge_schema(self, deal: SchemaDeal) -> None:
        self.status = deal.status

        if deal.user is not None:
            self._user_id = deal.user.id
            self._client._push_user_profile(deal.user)

        if deal.chat is not None:
            self._chat_id = deal.chat.id

    @property
    def user(self) -> "User | None":
        if not self._user_id:
            return None
        return self._client._get_user_identity(self._user_id)

    @property
    def chat(self) -> "Chat | None":
        if not self._chat_id:
            return None
        return self._client._get_chat_identity(self._chat_id)

    async def refresh(self) -> "Deal":
        await self._client._push_deal(self.id)
        return self

    async def complete(self) -> "Deal":
        # minimal "complete": CONFIRMED (IN) or SENT (OUT) depends on direction; we keep it simple.
        updated = await self._client.raw.deals.update_deal(self.id, ItemDealStatuses.CONFIRMED)
        if updated is not None:
            self._client._push_deal_schema(updated)
        return self
