import asyncio

from dotenv import load_dotenv

from aiosellers.playerok.models import ChatTypes, TransactionProviderIds, ItemDealDirections, ItemDealStatuses
from aiosellers.playerok.services.account import AccountService
from aiosellers.playerok.services.chats import ChatService
from aiosellers.playerok.services.deals import DealsService
from aiosellers.playerok.services.games import GamesService
from aiosellers.playerok.services.items import ItemsService

load_dotenv()


async def main():
    pass
    service = AccountService()
    me = await service.get_me()
    print("Me:", me)
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

    # service = GamesService()
    # optainings = await service.get_game_category_obtaining_types("1ecc48ce-52e6-6010-c327-d8c26efee5e3")
    # # # 1eef1f9b-96dd-6e00-7f93-28a08b9479ce
    # print(optainings.model_dump_json(indent=2))
    # return

    # options = await service.get_game_category_data_fields("1ecc48ce-52e6-6010-c327-d8c26efee5e3",
    #                                                       optainings.obtaining_types[0].id)
    # for option in options.data_fields:
    #     print(option.model_dump_json(indent=2))
    # options = await service.get_game_category("1ecc48ce-4f1a-6531-300d-9faaa8c3ab04", id="1ecc48ce-52e6-6010-c327-d8c26efee5e3")
    # print(options.model_dump_json(indent=2))

    # service = ItemsService()
    # resp = await service.create_item(
    #     game_category_id="1ecc48ce-52e6-6010-c327-d8c26efee5e3",
    #     obtaining_type_id="1eef1f9a-8b57-68c0-9481-cd3946f6e5de",
    #     name="My Test Item Name For Sellings",
    #     price=1200,
    #     description="Test Item Description",
    #     options={"server": "99-nights-in-the-forest"},
    #     data_fields={"1eef1f9c-595b-6ea0-2de0-9762c2db4d82": "Brainvrot Seller",
    #                  '1eef1f9c-2f96-68e0-bff0-d49bcb2e8549': 'Brainvrot Seller',
    #                  '1eef1fa1-a7e0-6ad0-b425-0d3c12f7fa82': "I'm the best seller"},
    #     attachments=["/Users/zewsic/projects/All-In-One-Sellers-API/p1.png",
    #                  "/Users/zewsic/projects/All-In-One-Sellers-API/p2.jpg"]
    # )
    # print(resp.model_dump_json(indent=2))
    #
    # resp_2 = await service.update_item(resp.id, price=500, remove_attachments=[resp.attachments[0].id])
    # print(resp_2.model_dump_json(indent=2))

    # cresp = await service.get_item_priority_statuses("1f0ec20d-faa6-6480-c7cc-e84b361c455a", 1000)
    # for item in cresp:
    #     print(item)

    # resp = await service.publish_item("1f0ec20d-faa6-6480-c7cc-e84b361c455a", cresp[-1].id)
    # print(resp.model_dump_json(indent=2))

    # resp = await service.increase_item_priority_status("1f0ec1ee-c7e0-6060-a889-a80ffd87cdac", cresp[0].id)
    # print(resp)

    # resp = await service.remove_item("1f0ec1e3-ca0a-63a0-b6c8-da49af296ceb")
    # print(resp)

    # resp_3 = await service.p


    # service = AccountService()
    # me = await service.get_me()
    # print("me:", me)
    #
    # service = ChatService()
    # chats = await service.get_chats(user_id=me.id)
    # print("chats:", chats.model_dump_json(indent=2))
    # chat = await service.get_chat("1f0e988b-a807-6450-7fa5-9553f54ced5a")
    # chat = chats.chats[0]
    # chat = await service.mark_chat_as_read(chat_id=chat.id)
    # print(chat)
    # print(chat.last_message.user.username, "> ", chat.last_message.text)
    # sent_message = await service.send_message(
    #     chat_id=chat.id,
    #     text="Это мы!!!",
    #     photo_path="/Users/zewsic/projects/All-In-One-Sellers-API/photo.png",
    # )
    # print(sent_message)
    # messages = await service.get_chat_messages(chat_id=chat.id)
    # print("Messages:", messages.model_dump_json(indent=2))

    # service = AccountService()
    # me = await service.get_me()
    #
    # service = ChatService()
    #
    # while 1:
    #     chats = await service.get_chats(user_id=me.id)
    #
    #     for chat in chats.chats:
    #         if chat.type != ChatTypes.PM or chat.unread_messages_counter == 0:
    #             continue
    #
    #         print(f'В чате с {chat.users[-1].username} непрочитанных сообщений: {chat.unread_messages_counter}')
    #
    #         messages = await service.get_chat_messages(chat_id=chat.id, count=chat.unread_messages_counter)
    #         for message in messages.messages:
    #             if message.file:
    #                 print(f'- [FILE] {message.file.url}')
    #                 continue
    #             elif message.text:
    #                 print(f'- [TEXT] {message.text}')
    #             else:
    #                 print(f'- [UNKNOWN]')
    #                 continue
    #
    #             if '/help' in message.text:
    #                 await service.send_message(chat_id=chat.id, text="Я пока что только учусь, команд пока нет :(")
    #             else:
    #                 await service.send_message(chat_id=chat.id, text="Привет! Я бот Dellonty, напиши команду /help чтобы узнать что я могу!")
    #
    #         await asyncio.sleep(1)
    #
    #         ValueError

    service = ItemsService()
    item = await service.get_item(slug='8ba135c7fb93-afon-pro-maks-luchshiy')
    print("Item:", item)

    service = DealsService()
    # deals = await service.get_deals(me.id, direction=ItemDealDirections.IN)
    # print(deals.model_dump_json(indent=2))

    # r = await service.get_deal("1f0ec20d-f997-6490-7877-eeba0c4a4925")
    # print(r.model_dump_json(indent=2))

    # r = await service.update_deal(deals.deals[0].id, ItemDealStatuses.CONFIRMED) # OUT-Confirm - SENT, OUT-Cancel - ROLL BACK. IN - CONFIRM - CONFIRMED
    # print(r)
    created = await service.create_deal(item.id, TransactionProviderIds.BANK_CARD_RU)
    print(created)

if __name__ == "__main__":
    asyncio.run(main())
