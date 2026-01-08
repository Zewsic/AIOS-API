from __future__ import annotations

from ..core.utils import _dig, _raise_on_gql_errors
from ..graphql import GraphQLQuery as GQL
from ..schemas import Game, GameCategoryInstructionTypes, GameList, GameType
from ..schemas.games import (
    GameCategory,
    GameCategoryAgreementList,
    GameCategoryDataFieldList,
    GameCategoryDataFieldTypes,
    GameCategoryInstructionList,
    GameCategoryObtainingTypeList,
)
from ..transport import PlayerokTransport


class RawGamesService:
    def __init__(self, transport: PlayerokTransport):
        self._transport = transport

    async def get_games(
        self, count: int = 24, type: GameType | None = None, cursor: str | None = None
    ) -> GameList | None:
        response = await self._transport.request(
            "post", "graphql", GQL.get_games(count=count, type=type, cursor=cursor)
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "games"))
        if data is None:
            return None
        return GameList(**data)

    async def get_game(self, id: str | None = None, slug: str | None = None) -> Game | None:
        if id is None and slug is None:
            raise ValueError("Can't get game without id or slug")

        response = await self._transport.request("post", "graphql", GQL.get_game(id=id, slug=slug))
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "game"))
        if data is None:
            return None
        return Game(**data)

    async def get_game_category(
        self, game_id: str | None = None, slug: str | None = None, id: str | None = None
    ) -> GameCategory | None:
        if id is None and slug is None and game_id is None:
            raise ValueError("Can't get game category without id or slug or game_id")

        response = await self._transport.request(
            "post", "graphql", GQL.get_game_category(game_id=game_id, slug=slug, id=id)
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "gameCategory"))
        if data is None:
            return None
        return GameCategory(**data)

    async def get_game_category_agreements(
        self,
        game_category_id: str,
        user_id: str,
        count: int = 24,
        cursor: str | None = None,
    ) -> GameCategoryAgreementList | None:
        if not game_category_id:
            raise ValueError("game_category_id is required")

        response = await self._transport.request(
            "post",
            "graphql",
            GQL.get_game_category_agreements(
                game_category_id=game_category_id,
                user_id=user_id,
                count=count,
                cursor=cursor,
            ),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "gameCategoryAgreements"))
        if data is None:
            return None
        return GameCategoryAgreementList(**data)

    async def get_game_category_obtaining_types(
        self,
        game_category_id: str,
        count: int = 24,
        cursor: str | None = None,
    ) -> GameCategoryObtainingTypeList | None:
        if not game_category_id:
            raise ValueError("game_category_id is required")

        response = await self._transport.request(
            "post",
            "graphql",
            GQL.get_game_category_obtaining_types(
                game_category_id=game_category_id,
                count=count,
                cursor=cursor,
            ),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "gameCategoryObtainingTypes"))
        if data is None:
            return None
        return GameCategoryObtainingTypeList(**data)

    async def get_game_category_instructions(
        self,
        game_category_id: str,
        obtaining_type_id: str,
        count: int = 24,
        type: GameCategoryInstructionTypes | None = None,
        cursor: str | None = None,
    ) -> GameCategoryInstructionList | None:
        if not game_category_id:
            raise ValueError("game_category_id is required")
        if not obtaining_type_id:
            raise ValueError("obtaining_type_id is required")

        response = await self._transport.request(
            "post",
            "graphql",
            GQL.get_game_category_instructions(
                game_category_id=game_category_id,
                obtaining_type_id=obtaining_type_id,
                count=count,
                type=type,
                cursor=cursor,
            ),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "gameCategoryInstructions"))
        if data is None:
            return None
        return GameCategoryInstructionList(**data)

    async def get_game_category_data_fields(
        self,
        game_category_id: str,
        obtaining_type_id: str,
        count: int = 24,
        type: GameCategoryDataFieldTypes | None = None,
        cursor: str | None = None,
    ) -> GameCategoryDataFieldList | None:
        if not game_category_id:
            raise ValueError("game_category_id is required")
        if not obtaining_type_id:
            raise ValueError("obtaining_type_id is required")

        response = await self._transport.request(
            "post",
            "graphql",
            GQL.get_game_category_data_fields(
                game_category_id=game_category_id,
                obtaining_type_id=obtaining_type_id,
                count=count,
                type=type,
                cursor=cursor,
            ),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "gameCategoryDataFields"))
        if data is None:
            return None
        return GameCategoryDataFieldList(**data)
