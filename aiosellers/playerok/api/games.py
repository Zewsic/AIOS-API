from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

from ..entities.game import (
    Game,
    GameCategory,
    GameCategoryAgreement,
    GameCategoryDataField,
    GameCategoryInstruction,
    GameCategoryObtainingType,
    GameCategoryOption,
    OptionValue,
)
from ..schemas import (
    GameCategoryDataFieldTypes,
    GameCategoryOptionTypes,
    GameType,
)

if TYPE_CHECKING:
    from ..playerok import Playerok


class GameAPI:
    def __init__(self, client: Playerok) -> None:
        self._client = client

    async def get_category(
        self,
        *,
        id: str | None = None,
        slug: str | None = None,
        game_id: str | None = None,
        force_refresh: bool = False,
    ) -> GameCategory | None:
        """Get a game category by id/slug/game_id.

        Note:
            This is a high-level wrapper over the raw service:
            `client._raw.games.get_game_category(...)`.

        Args:
            id: Category ID
            slug: Category slug
            game_id: Game ID (optional filter, depending on PlayerOK API behavior)
            force_refresh: Reserved for future caching. Currently has no effect.
        """
        _ = force_refresh  # reserved for future caching
        schema = await self._client._raw.games.get_game_category(game_id=game_id, slug=slug, id=id)
        if schema is None:
            return None

        category = GameCategory(
            id=schema.id,
            name=schema.name,
            slug=schema.slug,
            game_id=schema.game_id,
            game=None,
        )
        category._client = self._client
        return category

    def _create_game(self, schema) -> Game:
        if self._client._use_identity_map and hasattr(schema, "id"):
            cached = self._client._identity_maps.games.get(schema.id)
            if cached:
                return cached

        from ..entities.file import File

        game = Game(
            id=schema.id,
            name=schema.name,
            slug=schema.slug,
            type=schema.type,
            logo=File.from_schema(schema.logo) if schema.logo else None,
            categories=[],
        )
        game._client = self._client

        for cat_schema in schema.categories:
            category = GameCategory(
                id=cat_schema.id,
                name=cat_schema.name,
                slug=cat_schema.slug,
                game_id=game.id,
                game=game,
            )
            category._client = self._client
            game.categories.append(category)

        if self._client._use_identity_map:
            self._client._identity_maps.games.set(game.id, game)

        return game

    async def get(
        self, *, id: str | None = None, slug: str | None = None, force_refresh: bool = False
    ) -> Game | None:
        if id and not force_refresh and self._client._use_identity_map:
            cached = self._client._identity_maps.games.get(id)
            if cached:
                return cached

        schema = await self._client._raw.games.get_game(id, slug)
        if schema is None:
            return None

        return self._create_game(schema)

    async def list(
        self,
        *,
        limit: int = 24,
        cursor: str | None = None,
        type: GameType | None = None,
        search: str | None = None,
    ) -> list[Game]:
        result = []
        remain = limit
        current_cursor = cursor

        while remain > 0:
            response = await self._client._raw.games.get_games(
                count=min(24, remain),
                cursor=current_cursor,
                type=type,
                search=search,
            )
            if response is None or not response.games:
                break

            for schema in response.games:
                result.append(self._create_game(schema))

            remain -= len(response.games)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

        return result[:limit]

    async def iter(
        self,
        *,
        cursor: str | None = None,
        type: GameType | None = None,
        search: str | None = None,
    ) -> AsyncIterator[Game]:
        current_cursor = cursor

        while True:
            response = await self._client._raw.games.get_games(
                cursor=current_cursor,
                type=type,
                search=search,
            )
            if response is None or not response.games:
                return

            for schema in response.games:
                yield self._create_game(schema)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

    # --- Sub-entity methods ---

    async def get_category_options(self, category_id: str) -> list[GameCategoryOption]:
        raw_options = await self._client._raw.games.get_game_category_options(
            game_category_id=category_id
        )

        options_map = {}
        for option in raw_options:
            if option.field not in options_map:
                opt_obj = GameCategoryOption(
                    id=option.id,
                    type=option.type,
                    group_name=option.group,
                    slug=option.field,
                    possible_values=[],
                    category_id=category_id,
                )
                opt_obj._client = self._client
                options_map[option.field] = opt_obj

            option_object = options_map[option.field]

            if option.type is GameCategoryOptionTypes.SELECTOR:
                option_object.possible_values.append(
                    OptionValue(value=option.value, name=option.label, _option=option_object)
                )
            elif option.type is GameCategoryOptionTypes.RANGE:
                minimal_value = min(0, option.value_range_limit.min or 0)
                maximal_value = max(0, option.value_range_limit.max or 0)
                for i in range(minimal_value, maximal_value):
                    option_object.possible_values.append(
                        OptionValue(value=str(i), name=str(i), _option=option_object)
                    )
            elif option.type is GameCategoryOptionTypes.SWITCH:
                option_object.possible_values.append(
                    OptionValue(value="false", name="No", _option=option_object)
                )
                option_object.possible_values.append(
                    OptionValue(value="true", name="Yes", _option=option_object)
                )

        return list(options_map.values())

    async def get_obtaining_types(
        self, category_id: str, *, cursor: str | None = None, limit: int = 24
    ) -> list[GameCategoryObtainingType]:
        result = []
        remain = limit
        current_cursor = cursor

        while remain > 0:
            response = await self._client._raw.games.get_game_category_obtaining_types(
                game_category_id=category_id,
                cursor=current_cursor,
            )
            if response is None or not response.obtaining_types:
                break

            for schema in response.obtaining_types:
                obj = GameCategoryObtainingType(
                    id=schema.id,
                    name=schema.name,
                    description=schema.description,
                    category_id=category_id,
                )
                obj._client = self._client
                result.append(obj)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor
            remain -= len(response.obtaining_types)  # Approximate

        return result

    async def get_agreements(
        self,
        category_id: str,
        *,
        obtaining_type_id: str | None = None,
        cursor: str | None = None,
        limit: int = 24,
    ) -> list[GameCategoryAgreement]:
        result = []
        remain = limit
        current_cursor = cursor
        user_id = self._client._me_id

        while remain > 0:
            response = await self._client._raw.games.get_game_category_agreements(
                game_category_id=category_id,
                user_id=user_id,
                cursor=current_cursor,
                **({"obtaining_type_id": obtaining_type_id} if obtaining_type_id else {}),
            )
            if response is None or not response.agreements:
                break

            for schema in response.agreements:
                obj = GameCategoryAgreement(
                    id=schema.id,
                    description=schema.description,
                    type=schema.icon_type,
                    category_id=category_id,
                    obtaining_type_id=obtaining_type_id,
                )
                obj._client = self._client
                result.append(obj)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor
            remain -= len(response.agreements)

        return result

    async def accept_agreement(self, agreement_id: str) -> bool:
        resp = await self._client._raw.games.accept_game_category_agreement(
            agreement_id, self._client._me_id
        )
        return resp is not None

    async def get_instructions(
        self,
        category_id: str,
        obtaining_type_id: str,
        *,
        cursor: str | None = None,
        limit: int = 24,
    ) -> list[GameCategoryInstruction]:
        result = []
        remain = limit
        current_cursor = cursor

        while remain > 0:
            response = await self._client._raw.games.get_game_category_instructions(
                game_category_id=category_id,
                obtaining_type_id=obtaining_type_id,
                cursor=current_cursor,
            )
            if response is None or not response.instructions:
                break

            for schema in response.instructions:
                obj = GameCategoryInstruction(
                    id=schema.id,
                    text=schema.text,
                    category_id=category_id,
                    obtaining_type_id=obtaining_type_id,
                )
                obj._client = self._client
                result.append(obj)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor
            remain -= len(response.instructions)

        return result

    async def get_data_fields(
        self,
        category_id: str,
        obtaining_type_id: str,
        *,
        cursor: str | None = None,
        type: GameCategoryDataFieldTypes | None = None,
    ) -> list[GameCategoryDataField]:
        # Default to ITEM_DATA for seller flow (creating items)
        if type is None:
            type = GameCategoryDataFieldTypes.ITEM_DATA

        result = []
        current_cursor = cursor

        while True:
            response = await self._client._raw.games.get_game_category_data_fields(
                game_category_id=category_id,
                obtaining_type_id=obtaining_type_id,
                cursor=current_cursor,
                type=type,
            )
            if response is None or not response.data_fields:
                break

            for schema in response.data_fields:
                obj = GameCategoryDataField(
                    id=schema.id,
                    type=schema.type,
                    input_type=schema.input_type,
                    name=schema.label,
                    required=schema.required,
                )
                result.append(obj)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

        return result
