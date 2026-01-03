import asyncio

from dotenv import load_dotenv

from sellers.playerok.services.account import AccountService

load_dotenv()


async def main():
    service = AccountService()
    me = await service.get_me()
    print("Me:", me)
    account = await service.get_account(me.username)
    print("Account:", account)
    user = await service.get_user("Sen1a")
    print("User:", user)


if __name__ == "__main__":
    asyncio.run(main())
