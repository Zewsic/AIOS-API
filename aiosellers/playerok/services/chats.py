from ..core import PlayerokClient, _dig, _raise_on_gql_errors
from ..graphql import GraphQLQuery as GQL
from ..models import Chat, ChatList, ChatMessage, ChatMessageList, ChatStatuses, ChatTypes


class ChatService(PlayerokClient):
    async def get_chats(
        self,
        user_id: str | None = None,
        count: int = 24,
        type: ChatTypes | None = None,
        status: ChatStatuses | None = None,
        cursor: str | None = None,
    ) -> ChatList | None:
        response = await self.request(
            "post",
            "graphql",
            GQL.get_chats(user_id=user_id, count=count, type=type, status=status, cursor=cursor),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "chats"))

        if data is None:
            return None

        return ChatList(**data)

    async def get_chat(self, chat_id: str) -> Chat | None:
        response = await self.request(
            "post",
            "graphql",
            GQL.get_chat(chat_id=chat_id),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "chat"))

        if data is None:
            return None

        return Chat(**data)

    async def mark_chat_as_read(self, chat_id: str) -> Chat | None:
        response = await self.request(
            "post",
            "graphql",
            GQL.mark_chat_as_read(chat_id=chat_id),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "markChatAsRead"))

        if data is None:
            return None

        return Chat(**data)

    async def get_chat_messages(
        self, chat_id: str, count: int = 24, cursor: str | None = None
    ) -> ChatMessageList | None:
        response = await self.request(
            "post",
            "graphql",
            GQL.get_chat_messages(chat_id=chat_id, count=count, cursor=cursor),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "chatMessages"))

        if data is None:
            return None

        return ChatMessageList(**data)

    async def send_message(
        self,
        chat_id: str,
        text: str | None = None,
        photo_path: str | None = None,
        mark_as_read: bool = False,
    ) -> ChatMessage | None:
        if not text and not photo_path:
            raise ValueError("Either 'text' or 'photo_path' must be provided.")

        if mark_as_read:
            await self.mark_chat_as_read(chat_id=chat_id)
        if text and photo_path:
            await self.send_message(chat_id=chat_id, photo_path=photo_path)
            return await self.send_message(
                chat_id=chat_id, text=text
            )  # Can't send both text and photo

        if photo_path:
            payload = GQL.create_chat_message_with_photo(chat_id=chat_id, text=text)

            with open(photo_path, "rb") as f:
                files = {"1": f}
                response = await self.request("post", "graphql", payload, files=files)
        else:
            payload = GQL.create_chat_message(chat_id=chat_id, text=text)
            response = await self.request("post", "graphql", payload)

        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "createChatMessage"))

        if data is None:
            return None

        return ChatMessage(**data)
