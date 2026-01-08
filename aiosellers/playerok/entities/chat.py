from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, AsyncIterator

from ..schemas import ChatTypes
from ..schemas.chats import Chat as SchemaChat
from ..schemas.chats import ChatMessage as SchemaChatMessage

if TYPE_CHECKING:  # pragma: no cover
    from ..playerok import Playerok
    from .file import File
    from .user import User


@dataclass(slots=True)
class ChatMessage:
    id: str
    sent_at: datetime
    is_read: bool
    text: str | None = None
    file: File | None = None

    _client: "Playerok" = field(repr=False, default=None)
    _chat_id: str | None = field(repr=False, default=None)
    _user_id: str | None = field(repr=False, default=None)

    @classmethod
    def from_schema(cls, client: "Playerok", f: SchemaChatMessage, chat_id: str) -> ChatMessage:
        from .file import File

        return cls(
            id=f.id,
            sent_at=f.created_at,
            is_read=f.is_read,
            text=f.text,
            file=File.from_schema(f.file) if f.file else None,
            _client=client,
            _chat_id=chat_id,
            _user_id=f.user.id if f.user else None,
        )

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


@dataclass(slots=True)
class Chat:
    id: str
    type: ChatTypes = ChatTypes.PM
    unread_messages_counter: int | None = None

    _client: "Playerok" = field(repr=False, default=None)
    _user_id: str | None = field(repr=False, default=None)

    @classmethod
    def _create(cls, *, client: "Playerok", id: str) -> "Chat":
        return cls(id=id, _client=client)

    async def refresh(self) -> "Chat":
        await self._client._push_chat(self.id)
        return self

    def _merge_schema(self, chat: SchemaChat) -> None:
        self.unread_messages_counter = chat.unread_messages_counter
        self.type = chat.type

        # PM chat: "participants" contains both users, pick a non-self if possible.
        if chat.users:
            me_id = self._client.id
            other = None
            for u in chat.users:
                if me_id and u.id != me_id:
                    other = u
                    break
            if other is None:
                other = chat.users[0]
            self._user_id = other.id
            self._client._push_user_profile(other)

    @property
    def user(self) -> "User | None":
        if not self._user_id:
            return None
        return self._client._get_user_identity(self._user_id)

    async def send_photo(self, path: str, *, mark_as_read: bool = False) -> None:
        await self._client.raw.chats.send_message(
            self.id, photo_path=path, mark_as_read=mark_as_read
        )

    async def send_text(self, text: str, *, mark_as_read: bool = False) -> None:
        await self._client.raw.chats.send_message(self.id, text=text, mark_as_read=mark_as_read)

    async def iter_messages(
        self,
        *,
        cursor: str | None = None,
    ) -> AsyncIterator[ChatMessage]:
        while True:
            messages = await self._client.raw.chats.get_chat_messages(
                chat_id=self.id,
                after_cursor=cursor,
            )
            if messages is None:
                return
            for message in messages.messages:
                yield ChatMessage.from_schema(self._client, message, self.id)
            if not messages.page_info.has_next_page:
                break
            cursor = messages.page_info.end_cursor

    async def get_messages(
        self, *, count: int = 24, cursor: str | None = None
    ) -> list[ChatMessage]:
        remain = count
        resp = []
        while remain > 0:
            messages = await self._client.raw.chats.get_chat_messages(
                chat_id=self.id,
                after_cursor=cursor,
            )
            if messages is None:
                break
            for message in messages.messages:
                resp.append(ChatMessage.from_schema(self._client, message, self.id))
            if not messages.page_info.has_next_page:
                break
            cursor = messages.page_info.end_cursor
            remain -= min(24, remain)

        return resp
