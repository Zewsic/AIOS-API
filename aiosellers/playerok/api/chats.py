"""Chats API module."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, AsyncIterator

from ..entities.chat import Chat, ChatMessage
from ..entities.file import File
from ..schemas import ChatStatuses, ChatTypes

if TYPE_CHECKING:
    from ..playerok import Playerok


class ChatMessagesAPI:
    """Chat messages API."""

    def __init__(self, client: Playerok) -> None:
        self._client = client

    async def list(
        self, chat_id: str, *, limit: int = 50, cursor: str | None = None
    ) -> list[ChatMessage]:
        """Get messages from a chat.

        Args:
            chat_id: Chat ID to fetch messages from.
            limit: Maximum number of messages to fetch.
            cursor: Pagination cursor.

        Returns:
            List of ChatMessage objects.
        """
        result = []
        remain = limit
        current_cursor = cursor

        while remain > 0:
            response = await self._client._raw.chats.get_chat_messages(
                chat_id=chat_id, count=min(50, remain), after_cursor=current_cursor
            )
            if response is None or not response.messages:
                break

            for msg in response.messages:
                result.append(
                    ChatMessage(
                        id=msg.id,
                        sent_at=msg.created_at,
                        is_read=msg.is_read,
                        text=msg.text,
                        file=File.from_schema(msg.file) if msg.file else None,
                        user_id=msg.user.id if msg.user else None,
                        chat_id=chat_id,
                    )
                )

            remain -= len(response.messages)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

        return result[:limit]

    async def iter(self, chat_id: str, *, cursor: str | None = None) -> AsyncIterator[ChatMessage]:
        """Iterate over all messages in a chat.

        Args:
            chat_id: Chat ID to fetch messages from.
            cursor: Starting pagination cursor.

        Yields:
            ChatMessage objects.
        """
        current_cursor = cursor

        while True:
            response = await self._client._raw.chats.get_chat_messages(
                chat_id=chat_id, after_cursor=current_cursor
            )
            if response is None or not response.messages:
                return

            for msg in response.messages:
                yield ChatMessage(
                    id=msg.id,
                    sent_at=msg.created_at,
                    is_read=msg.is_read,
                    text=msg.text,
                    file=File.from_schema(msg.file) if msg.file else None,
                    user_id=msg.user.id if msg.user else None,
                    chat_id=chat_id,
                )

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor


class ChatAPI:
    """Chat-related API methods."""

    def __init__(self, client: Playerok) -> None:
        self._client = client
        self.messages = ChatMessagesAPI(client)

    async def get(self, chat_id: str, *, force_refresh: bool = False) -> Chat | None:
        """Get chat by ID.

        Args:
            chat_id: Chat ID to fetch.
            force_refresh: If True, bypass identity map and fetch fresh data.

        Returns:
            Chat entity with client attached, or None if not found.
        """
        # Check identity map first
        if not force_refresh and self._client._use_identity_map:
            cached = self._client._identity_maps.chats.get(chat_id)
            if cached:
                return cached

        # Fetch from API
        schema = await self._client._raw.chats.get_chat(chat_id)
        if schema is None:
            return None

        # Determine user_id from participants
        user_id = None
        if schema.users:
            me_id = self._client._me_id
            for u in schema.users:
                if me_id and u.id != me_id:
                    user_id = u.id
                    # Also push user to identity map
                    if self._client._use_identity_map:
                        user = self._client.account.get_user(u.id)
                    break
            if user_id is None:
                user_id = schema.users[0].id

        chat = Chat(
            id=schema.id,
            type=schema.type,
            unread_messages_counter=schema.unread_messages_counter,
            user_id=user_id,
        )

        # Attach client
        chat._client = self._client

        # Store in identity map
        if self._client._use_identity_map:
            self._client._identity_maps.chats.set(chat_id, chat)

        return chat

    async def list(
        self,
        *,
        limit: int = 24,
        cursor: str | None = None,
        type: ChatTypes | None = None,
        status: ChatStatuses | None = None,
    ) -> list[Chat]:
        """Get list of chats.

        Args:
            limit: Maximum number of chats to fetch.
            cursor: Pagination cursor.
            type: Filter by chat type.
            status: Filter by chat status.

        Returns:
            List of Chat entities.
        """
        result = []
        remain = limit
        current_cursor = cursor

        while remain > 0:
            response = await self._client._raw.chats.get_chats(
                user_id=self._client._me_id,
                count=min(24, remain),
                cursor=current_cursor,
                type=type,
                status=status,
            )
            if response is None or not response.chats:
                break

            for schema in response.chats:
                # Determine user_id
                user_id = None
                if schema.users:
                    me_id = self._client._me_id
                    for u in schema.users:
                        if me_id and u.id != me_id:
                            user_id = u.id
                            break
                    if user_id is None:
                        user_id = schema.users[0].id

                chat = Chat(
                    id=schema.id,
                    type=schema.type,
                    unread_messages_counter=schema.unread_messages_counter,
                    user_id=user_id,
                )
                chat._client = self._client

                if self._client._use_identity_map:
                    self._client._identity_maps.chats.set(schema.id, chat)

                result.append(chat)

            remain -= len(response.chats)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

        return result[:limit]

    async def iter(
        self,
        *,
        cursor: str | None = None,
        type: ChatTypes | None = None,
        status: ChatStatuses | None = None,
    ) -> AsyncIterator[Chat]:
        """Iterate over all chats.

        Args:
            cursor: Starting pagination cursor.
            type: Filter by chat type.
            status: Filter by chat status.

        Yields:
            Chat entities.
        """
        current_cursor = cursor

        while True:
            response = await self._client._raw.chats.get_chats(
                user_id=self._client._me_id,
                cursor=current_cursor,
                type=type,
                status=status,
            )
            if response is None or not response.chats:
                return

            for schema in response.chats:
                user_id = None
                if schema.users:
                    me_id = self._client._me_id
                    for u in schema.users:
                        if me_id and u.id != me_id:
                            user_id = u.id
                            break
                    if user_id is None:
                        user_id = schema.users[0].id

                chat = Chat(
                    id=schema.id,
                    type=schema.type,
                    unread_messages_counter=schema.unread_messages_counter,
                    user_id=user_id,
                )
                chat._client = self._client

                if self._client._use_identity_map:
                    self._client._identity_maps.chats.set(schema.id, chat)

                yield chat

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

    async def send_message(
        self,
        chat_id: str,
        *,
        text: str | None = None,
        photo: str | Path | None = None,
        mark_as_read: bool = False,
    ) -> ChatMessage:
        """Send message to a chat.

        Args:
            chat_id: Chat ID to send message to.
            text: Text content of the message.
            photo: Path to photo file to send.
            mark_as_read: Mark chat as read after sending.

        Returns:
            Sent ChatMessage object.

        Raises:
            ValueError: If neither text nor photo is provided.
        """
        if text is None and photo is None:
            raise ValueError("Either text or photo must be provided")

        msg = await self._client._raw.chats.send_message(
            chat_id=chat_id,
            text=text,
            photo_path=str(photo) if photo else None,
            mark_as_read=mark_as_read,
        )

        return ChatMessage(
            id=msg.id,
            sent_at=msg.created_at,
            is_read=msg.is_read,
            text=msg.text,
            file=File.from_schema(msg.file) if msg.file else None,
            user_id=msg.user.id if msg.user else None,
            chat_id=chat_id,
        )

    async def mark_as_read(self, chat_id: str) -> None:
        """Mark chat as read.

        Args:
            chat_id: Chat ID to mark as read.
        """
        await self._client._raw.chats.mark_chat_as_read(chat_id)
