from pydantic import BaseModel

from ..core import PlayerokClient
from ..core.exceptions import Unauthorized
from ..graphql import GraphQLQuery as GQL
from ..models import Account, UserProfile, AccountProfile


class AccountService(PlayerokClient):
    async def get_me(self) -> Account:
        response = await self.request("post", "graphql", GQL.get_me())
        data: dict = response.json()["data"]["viewer"]
        if data is None:
            raise Unauthorized()

        return Account(**data)

    async def get_account(self, username: str | None = None) -> AccountProfile:
        if username is None:
            raise ValueError("Can't get account with no username")
        response = await self.request("post", "graphql", GQL.get_user(username=username))

        data = response.json()["data"]["user"]
        if data.get("__typename") == "User":
            profile = data
        else:
            profile = None

        return AccountProfile(**profile)

    async def get_user(
        self, username: str | None = None, id: str | None = None
    ) -> UserProfile:
        if username is None and id is None:
            raise ValueError("Can't get user with no username or id")
        response = await self.request("post", "graphql", GQL.get_user(username=username, id=id))

        data = response.json()["data"]["user"]
        if data.get("__typename") == "UserFragment":
            profile = data
        elif data.get("__typename") == "User":
            profile = data.get("profile")
        else:
            profile = None

        return UserProfile(**profile)


