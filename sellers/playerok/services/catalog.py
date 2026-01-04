import json

from pydantic import BaseModel

from ..core import PlayerokClient
from ..core.exceptions import Unauthorized
from ..graphql import GraphQLQuery as GQL
from ..models import GameList, GameType


class CatalogService(PlayerokClient):
    async def get_games(
        self, count: int = 24, type: GameType | None = None, cursor: str | None = None
    ) -> GameList:
        response = await self.request(
            "post", "graphql", GQL.get_games(count, type, cursor)
        )
        data: dict = response.json()["data"]["games"]
        if data is None:
            return None

        print(json.dumps(data, indent=2))

        return GameList(**data)
