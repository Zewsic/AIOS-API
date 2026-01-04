from ..core import PlayerokClient, _dig, _raise_on_gql_errors
from ..core.exceptions import Unauthorized
from ..graphql import GraphQLQuery as GQL
from ..models import Account, AccountProfile, UserProfile


class AccountService(PlayerokClient):
    async def get_me(self) -> Account:
        response = await self.request("post", "graphql", GQL.get_me())
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "viewer"))
        if data is None:
            raise Unauthorized()

        return Account(**data)

    async def get_account(self, username: str | None = None) -> AccountProfile | None:
        if username is None:
            raise ValueError("Can't get account with no username")
        response = await self.request("post", "graphql", GQL.get_user(username=username))
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "user"))
        if data.get("__typename") == "User":
            profile = data
        else:
            return None

        return AccountProfile(**profile)

    async def get_user(
        self, username: str | None = None, id: str | None = None
    ) -> UserProfile | None:
        if username is None and id is None:
            raise ValueError("Can't get user with no username or id")
        response = await self.request("post", "graphql", GQL.get_user(username=username, id=id))
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "user"))
        if data.get("__typename") == "UserFragment":
            profile = data
        elif data.get("__typename") == "User":
            profile = data.get("profile")
        else:
            return None

        return UserProfile(**profile)
