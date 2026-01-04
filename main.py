import asyncio

from dotenv import load_dotenv

from aiosellers.playerok.services.account import AccountService
from aiosellers.playerok.services.chats import ChatService

load_dotenv()


async def main():
    # service = AccountService()
    # me = await service.get_me()
    # print("Me:", me)
    # account = await service.get_account(me.username)
    # print("Account:", account)
    # user = await service.get_user("Sen1a")
    # print("User:", user)

    # service = GamesService()
    # games = await service.get_games(count=1, type=GameType.APPLICATION)
    # print("games:", games)
    # category = await service.get_game_category(games.games[0].id, "stars")
    # print("category:", category)
    # game = await service.get_game(slug="telegram")
    # print("game:", game)
    # agreements = await service.get_game_category_agreements(category.id, user_id=user.id)
    # print("agreements:", agreements)
    # obtainnings = await service.get_game_category_obtaining_types(category.id)
    # print("obtainings:", obtainnings)

    # cursor = None
    # for _ in range(10):
    #     games = await service.get_games(count=1, type=GameType.APPLICATION, cursor=cursor)
    #     print(f"games p{_}:", games)
    #     cursor = games.page_info.end_cursor

    # service = ItemsService()
    # items = await service.get_items(
    #     count=24,
    #     game_id="1ecc48ce-4f1a-6531-300d-9faaa8c3ab04",
    #     category_id="1ecc48ce-52e6-6010-c327-d8c26efee5e3",
    #     attributes=[{"field": "server", "value": "steal-a-brainrot", "type": "SELECTOR"}],
    # )
    # for item in items.items:
    #     print(item.name, " — ", item.price, "RUB")

    service = AccountService()
    me = await service.get_me()
    # print("me:", me)
    #
    service = ChatService()
    chats = await service.get_chats(user_id=me.id)
    # print("chats:", chats.model_dump_json(indent=2))
    # chat = await service.get_chat("1f0e988b-a807-6450-7fa5-9553f54ced5a")
    chat = chats.chats[0]
    # chat = await service.mark_chat_as_read(chat_id=chat.id)
    # print(chat)
    # print(chat.last_message.user.username, "> ", chat.last_message.text)
    sent_message = await service.send_message(
        chat_id=chat.id,
        text="Это мы!!!",
        photo_path="/Users/zewsic/projects/All-In-One-Sellers-API/photo.png",
    )
    print(sent_message)
    # messages = await service.get_chat_messages(chat_id=chat.id)
    # print("Messages:", messages.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
