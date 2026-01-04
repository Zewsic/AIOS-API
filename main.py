import asyncio

from dotenv import load_dotenv

from sellers.playerok.models import GameType
from sellers.playerok.services.account import AccountService
from sellers.playerok.services.games import GamesService

load_dotenv()


async def main():
    service = AccountService()
    me = await service.get_me()
    print("Me:", me)
    account = await service.get_account(me.username)
    print("Account:", account)
    user = await service.get_user("Sen1a")
    print("User:", user)

    service = GamesService()
    games = await service.get_games(count=1, type=GameType.APPLICATION)
    print("games:", games)
    category = await service.get_game_category(games.games[0].id, 'stars')
    print("category:", category)
    game = await service.get_game(slug='telegram')
    print("game:", game)
    agreements = await service.get_game_category_agreements(category.id, user_id=user.id)
    print("agreements:", agreements)
    obtainnings = await service.get_game_category_obtaining_types(category.id)
    print("obtainings:", obtainnings)


if __name__ == "__main__":
    asyncio.run(main())
