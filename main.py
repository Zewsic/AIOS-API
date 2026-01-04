import asyncio
from gettext import Catalog

from dotenv import load_dotenv

from sellers.playerok.models import GameType
from sellers.playerok.services.account import AccountService
from sellers.playerok.services.catalog import CatalogService

load_dotenv()


async def main():
    # service = AccountService()
    # me = await service.get_me()
    # print("Me:", me)
    # account = await service.get_account(me.username)
    # print("Account:", account)
    # user = await service.get_user("Sen1a")
    # print("User:", user)

    service = CatalogService()
    games = await service.get_games(count=24, type=GameType.APPLICATION)
    print("games:", games)



if __name__ == "__main__":
    asyncio.run(main())
