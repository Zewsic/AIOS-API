"""Example usage of refactored PlayerOK API."""

import asyncio

from dotenv import load_dotenv

from aiosellers.playerok import Playerok, PlayerokClientConfig

load_dotenv()


async def main() -> None:
    """Demo of new modular API."""
    # Option 1: Use config object
    config = PlayerokClientConfig(
        # access_token="..."  # or use PLAYEROK_ACCESS_TOKEN env var
        use_identity_map=True,
        request_timeout=15.0,
    )

    async with Playerok(config) as client:
        # Test some features

        async for item in client.items.iter_self():
            print(item)

        return

        # === Account API ===
        me = await client.account.me()
        profile = await client.account.profile()
        print(f"Logged in as: {me.username} (ID: {me.id})")
        print(f"Balance: {profile.balance} RUB")

        # === Chats API ===
        print("\n=== Chats ===")
        chats = await client.chats.list(limit=5)
        print(f"Found {len(chats)} chats")

        for chat in chats:
            if chat.type != "PM":
                continue
            print(f"  Chat {chat.id} - Type: {chat.type}")
            if chat.unread_messages_counter:
                print(f"    Unread: {chat.unread_messages_counter}")
                unread = await chat.get_messages(chat.unread_messages_counter)
                for message in unread:
                    print(f"      Message: {message.text}")

                deals = await chat.get_deals()
                print(f"    Deals: {len(deals)}")
                for deal in deals:
                    print(f"      Deal {deal.id} - Status: {deal.status}")

        # Get specific chat and use entity methods
        if chats:
            chat = chats[0]
            # Option 1: Entity method (convenient)
            # await chat.send_text("Hello from refactored API!")

            # Option 2: Client method (explicit)
            # await client.chats.send_message(chat.id, text="Hello!")

            # Get messages
            messages = await chat.get_messages(limit=3)
            print(f"\n  Last {len(messages)} messages in chat {chat.id}:")
            for msg in messages:
                print(f"    {msg.sent_at}: {msg.text or '[file]'}")

        # === Deals API ===
        print("\n=== Deals ===")
        deals = await client.deals.list(limit=5)
        print(f"Found {len(deals)} deals")

        for deal in deals:
            print(f"  Deal {deal.id} - Status: {deal.status}")
            # Entity methods for deals
            # await deal.confirm()  # Convenient!
            # await deal.refund()

        # Bulk operations example
        # pending_deals = await client.deals.list(
        #     statuses=[ItemDealStatuses.PENDING], limit=10
        # )
        # for deal in pending_deals:
        #     await deal.confirm()  # Easy bulk confirmation!

        # === Games API ===
        print("\n=== Games ===")
        games = await client.games.list(limit=24)
        print(f"Found {len(games)} games")

        for game in games[3:]:
            print(f"  Game: {game.name} ({game.slug})")
            print(f"    Categories: {len(game.categories)}")

            if game.categories:
                for category in game.categories:
                    print(f"      - {category.name}")

                    for option in await category.get_options():
                        print(f"        Option: {option.group_name}")

                    # Get obtaining types for category
                    obtaining_types = await category.get_obtaining_types()
                    for ot in obtaining_types:
                        print(f"        Obtaining: {ot.name}")

                        for data_field in await ot.get_data_fields():
                            print(f"          + Data Field: {data_field.name}")


if __name__ == "__main__":
    asyncio.run(main())
