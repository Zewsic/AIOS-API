from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncIterator

from .cache import AsyncTTLCache
from .entities import Chat, Deal, User
from .raw import RawAPI
from .schemas import Account
from .schemas.account import AccountProfile
from .schemas.account import UserProfile as SchemaUserProfile
from .schemas.chats import Chat as SchemaChat
from .schemas.deals import ItemDeal as SchemaDeal
from .schemas.enums import ChatStatuses, ChatTypes, ItemDealDirections, ItemDealStatuses
from .transport import PlayerokTransport


@dataclass(slots=True)
class _Caches:
    users: AsyncTTLCache[str, Any]
    chats: AsyncTTLCache[str, Any]
    deals: AsyncTTLCache[str, Any]
    items: AsyncTTLCache[str, Any]
    transactions: AsyncTTLCache[str, Any]
    files: AsyncTTLCache[str, Any]


class Playerok:
    """
    High-level client facade.

    This class owns:
    - one transport (shared TLS client)
    - raw low-level API (`self.raw`)
    - caches (identity map + TTL)
    """

    def __init__(self, access_token: str | None = None):
        self._access_token = access_token
        self.transport: PlayerokTransport | None = None
        self.raw: RawAPI | None = None
        self.me: Account | None = None
        self.profile: AccountProfile | None = None

        ttl = 300.0
        self.cache = _Caches(
            users=AsyncTTLCache(ttl),
            chats=AsyncTTLCache(ttl),
            deals=AsyncTTLCache(ttl),
            items=AsyncTTLCache(ttl),
            transactions=AsyncTTLCache(ttl),
            files=AsyncTTLCache(ttl),
        )

    async def __aenter__(self) -> "Playerok":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        await self.close()

    async def start(self) -> None:
        if self.transport is not None:
            return
        self.transport = PlayerokTransport(access_token=self._access_token)
        self.raw = RawAPI(self.transport)
        self.me = await self.raw.account.get_me()
        self.profile = await self.raw.account.get_account(self.me.username)

        # identity-map: create "me" as User entity too (optional convenience)
        self._get_user_identity(self.me.id)._merge_profile(
            SchemaUserProfile.model_validate(
                {"id": self.me.id, "username": self.me.username, "role": self.me.role}
            )
        )

    async def close(self) -> None:
        if self.transport is None:
            return
        await self.transport.close()
        self.transport = None
        self.raw = None

    # convenience proxies (me.*)
    @property
    def id(self) -> str | None:
        return self.me.id if self.me else None

    @property
    def username(self) -> str | None:
        return self.me.username if self.me else None

    @property
    def email(self) -> str | None:
        return self.me.email if self.me else None

    @property
    def balance(self) -> float | None:
        return self.profile.balance if self.profile else None

    # --------------------
    # identity-map helpers
    # --------------------
    def _get_user_identity(self, user_id: str) -> User:
        return self.cache.users.get_or_create(
            user_id, lambda: User._create(client=self, id=user_id)
        )

    def _get_chat_identity(self, chat_id: str) -> Chat:
        return self.cache.chats.get_or_create(
            chat_id, lambda: Chat._create(client=self, id=chat_id)
        )

    def _get_deal_identity(self, deal_id: str) -> Deal:
        return self.cache.deals.get_or_create(
            deal_id, lambda: Deal._create(client=self, id=deal_id)
        )

    def _push_user_profile(self, profile: SchemaUserProfile) -> User:
        user = self._get_user_identity(profile.id)
        user._merge_profile(profile)
        self.cache.users.touch(profile.id)
        return user

    def _push_chat_schema(self, chat: SchemaChat) -> Chat:
        entity = self._get_chat_identity(chat.id)
        entity._merge_schema(chat)
        self.cache.chats.touch(chat.id)
        return entity

    def _push_deal_schema(self, deal: SchemaDeal) -> Deal:
        entity = self._get_deal_identity(deal.id)
        entity._merge_schema(deal)
        self.cache.deals.touch(deal.id)
        return entity

    # --------------------
    # high-level get
    # --------------------
    async def get_user(self, user_id: str) -> User:
        async def fetch() -> User:
            profile = await self.raw.account.get_user(id=user_id)
            if profile is not None:
                return self._push_user_profile(profile)
            return self._get_user_identity(user_id)

        return await self.cache.users.get_or_fetch(user_id, fetch)

    async def _push_user(self, user_id: str) -> User:
        profile = await self.raw.account.get_user(id=user_id)
        if profile is not None:
            return self._push_user_profile(profile)
        return self._get_user_identity(user_id)

    async def get_deal(self, deal_id: str) -> Deal | None:
        async def fetch() -> Deal | None:
            deal = await self.raw.deals.get_deal(deal_id)
            if deal is None:
                return None
            return self._push_deal_schema(deal)

        return await self.cache.deals.get_or_fetch(deal_id, fetch)

    async def _push_deal(self, deal_id: str) -> Deal | None:
        deal = await self.raw.deals.get_deal(deal_id)
        if deal is None:
            return None
        return self._push_deal_schema(deal)

    async def get_chat(self, chat_id: str) -> Chat | None:
        async def fetch() -> Chat | None:
            chat = await self.raw.chats.get_chat(chat_id)
            if chat is None:
                return None
            return self._push_chat_schema(chat)

        return await self.cache.chats.get_or_fetch(chat_id, fetch)

    async def _push_chat(self, deal_id: str) -> Chat | None:
        deal = await self.raw.chats.get_chat(deal_id)
        if deal is None:
            return None
        return self._push_chat_schema(deal)

    # --------------------
    # iterators / queries
    # --------------------
    async def iter_chats(
        self,
        *,
        type: ChatTypes | None = None,
        status: ChatStatuses | None = None,
        cursor: str | None = None,
    ) -> AsyncIterator[Chat]:
        while True:
            chats = await self.raw.chats.get_chats(
                user_id=self.id, type=type, status=status, cursor=cursor
            )
            if chats is None:
                return
            for c in chats.chats:
                yield self._push_chat_schema(c)
            if not chats.page_info.has_next_page:
                return
            cursor = chats.page_info.end_cursor

    async def get_chats(
        self,
        *,
        count: int = 24,
        cursor: str | None = None,
        type: ChatTypes | None = None,
        status: ChatStatuses | None = None,
    ) -> list[Chat]:
        remain = count
        resp = []
        while remain > 0:
            chats = await self.raw.chats.get_chats(
                count=min(24, remain), user_id=self.id, type=type, status=status, cursor=cursor
            )
            if chats is None:
                break
            for c in chats.chats:
                resp.append(self._push_chat_schema(c))
            if not chats.page_info.has_next_page:
                break
            cursor = chats.page_info.end_cursor
            remain -= min(24, remain)
        return resp

    async def iter_deals(
        self,
        *,
        statuses: list[ItemDealStatuses] | None = None,
        direction: ItemDealDirections | None = None,
        cursor: str | None = None,
    ) -> AsyncIterator[Deal]:
        while True:
            deals = await self.raw.deals.get_deals(
                user_id=self.id,
                statuses=statuses,
                direction=direction,
                after_cursor=cursor,
            )
            if deals is None:
                return
            for d in deals.deals:
                yield self._push_deal_schema(d)
            if not deals.page_info.has_next_page:
                return
            cursor = deals.page_info.end_cursor

    async def get_deals(
        self,
        *,
        count: int = 24,
        cursor: str | None = None,
        statuses: list[ItemDealStatuses] | None = None,
        direction: ItemDealDirections | None = None,
    ) -> list[Deal]:
        remain = count
        resp = []
        while remain > 0:
            deals = await self.raw.deals.get_deals(
                count=min(24, remain),
                user_id=self.id,
                statuses=statuses,
                direction=direction,
                after_cursor=cursor,
            )
            if deals is None:
                break
            for d in deals.deals:
                resp.append(self._push_deal_schema(d))
            if not deals.page_info.has_next_page:
                break
            cursor = deals.page_info.end_cursor
            remain -= min(24, remain)
        return resp
