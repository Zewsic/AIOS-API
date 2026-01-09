from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, AsyncIterator

from ..schemas import (
    GameCategoryAgreementIconTypes,
    GameCategoryDataFieldInputTypes,
    GameCategoryDataFieldTypes,
    GameCategoryOptionTypes,
    GameType,
)
from ..schemas.games import (
    Game as SchemaGame,
)
from ..schemas.games import (
    GameCategory as SchemaGameCategory,
)
from ..schemas.games import (
    GameCategoryAgreement as SchemaGameCategoryAgreement,
)
from ..schemas.games import (
    GameCategoryInstruction as SchemaGameCategoryInstruction,
)
from ..schemas.games import (
    GameCategoryObtainingType as SchemaGameCategoryObtainingType,
)
from . import File

if TYPE_CHECKING:
    from aiosellers.playerok import Playerok


@dataclass(slots=True)
class OptionValue:
    name: str
    value: str

    _option: "GameCategoryOption"

    def select(self):
        return self._option.set_value(self)

    def __repr__(self):
        return f"OptionSelectorValue(name='{self.name}', value='{self.value}')"


@dataclass(slots=True)
class GameCategoryOption:
    id: str
    type: GameCategoryOptionTypes
    group_name: str
    slug: str
    possible_values: list["OptionValue"] | list

    _input_value: int | str | bool | None = None

    def set_value(self, value: int | str | bool | "OptionValue" | None) -> GameCategoryOption:
        if value in self.possible_values:
            if type(value) is OptionValue:
                self._input_value = value.value
            else:
                self._input_value = str(value).lower()
        else:
            raise ValueError(f"Invalid value {value}")
        return self


@dataclass(slots=True)
class GameCategoryDataField:
    id: str
    type: GameCategoryDataFieldTypes
    input_type: GameCategoryDataFieldInputTypes
    name: str
    required: bool

    _input_value: str | None = None

    def set_value(self, value: str) -> GameCategoryDataField:
        self._input_value = value
        return self


@dataclass(slots=True)
class GameCategoryAgreement:
    id: str
    description: str
    type: GameCategoryAgreementIconTypes

    game_category: "GameCategory" = field(repr=False, default=None)
    obtaining_type: "GameCategoryObtainingType" = field(repr=False, default=None)
    _client: "Playerok" = field(repr=False, default=None)

    @classmethod
    def from_schema(
        cls,
        f: SchemaGameCategoryAgreement,
        game_category: "GameCategory" = None,
        obtaining_type: "GameCategoryObtainingType" = None,
        client: "Playerok" = None,
    ) -> "GameCategoryAgreement":
        return cls(
            id=f.id,
            description=f.description,
            game_category=game_category,
            obtaining_type=obtaining_type,
            _client=client,
            type=f.icon_type,
        )

    async def accept(self, *, skip_waiting: bool = False) -> "GameCategoryAgreement":
        "PLEASE CALL ASYNCIO WAIT AFTER EXECUTING"
        resp = await self._client.raw.games.accept_game_category_agreement(self.id, self._client.id)

        if not skip_waiting:
            await asyncio.sleep(0.2)
        return resp is not None


@dataclass(slots=True)
class GameCategoryInstruction:
    id: str
    text: str

    game_category: "GameCategory" = field(repr=False, default=None)
    obtaining_type: GameCategoryObtainingType = field(repr=False, default=None)

    @classmethod
    def from_schema(
        cls,
        f: SchemaGameCategoryInstruction,
        game_category: "GameCategory" = None,
        obtaining_type: "GameCategoryObtainingType" = None,
    ) -> "GameCategoryInstruction":
        return cls(id=f.id, text=f.text, game_category=game_category, obtaining_type=obtaining_type)


@dataclass(slots=True)
class GameCategoryObtainingType:
    id: str
    name: str
    description: str

    game_category: "GameCategory" = field(repr=False, default=None)
    _client: "Playerok" = field(repr=False, default=None)

    @classmethod
    def from_schema(
        cls,
        f: SchemaGameCategoryObtainingType,
        game_category: "GameCategory" = None,
        client: "Playerok" = None,
    ) -> "GameCategoryObtainingType":
        return cls(
            id=f.id,
            name=f.name,
            description=f.description,
            game_category=game_category,
            _client=client,
        )

    async def iter_instructions(
        self,
        *,
        cursor: str | None = None,
    ) -> AsyncIterator[GameCategoryInstruction]:
        while True:
            instructions = await self._client.raw.games.get_game_category_instructions(
                game_category_id=self.id,
                obtaining_type_id=self.id,
                cursor=cursor,
            )
            if instructions is None:
                return
            for arg in instructions.instructions:
                yield GameCategoryInstruction.from_schema(
                    arg, game_category=self.game_category, obtaining_type=self
                )
            if not instructions.page_info.has_next_page:
                return
            cursor = instructions.page_info.end_cursor

    async def get_instructions(
        self, *, count: int = 24, cursor: str | None = None
    ) -> list[GameCategoryInstruction]:
        remain = count
        resp = []
        while remain > 0:
            instructions = await self._client.raw.games.get_game_category_instructions(
                game_category_id=self.game_category.id,
                obtaining_type_id=self.id,
                cursor=cursor,
            )
            if instructions is None:
                break
            for arg in instructions.instructions:
                resp.append(
                    GameCategoryInstruction.from_schema(
                        arg, game_category=self.game_category, obtaining_type=self
                    )
                )
            if not instructions.page_info.has_next_page:
                break
            cursor = instructions.page_info.end_cursor
            remain -= min(24, remain)

        return resp

    async def get_data_fields(self) -> list[GameCategoryDataField]:
        resp = []
        cursor = None
        while True:
            data_fields = await self._client.raw.games.get_game_category_data_fields(
                game_category_id=self.game_category.id,
                obtaining_type_id=self.id,
                cursor=cursor,
            )
            if data_fields is None:
                break
            for arg in data_fields.data_fields:
                resp.append(
                    GameCategoryDataField(
                        id=arg.id,
                        type=arg.type,
                        input_type=arg.input_type,
                        name=arg.label,
                        required=arg.required,
                    )
                )
            if not data_fields.page_info.has_next_page:
                break
            cursor = data_fields.page_info.end_cursor

        return resp

    async def iter_agreements(
        self,
        *,
        cursor: str | None = None,
    ) -> AsyncIterator[GameCategoryAgreement]:
        while True:
            agreements = await self._client.raw.games.get_game_category_agreements(
                game_category_id=self.id,
                obtaining_type_id=self.id,
                user_id=self._client.id,
                cursor=cursor,
            )
            if agreements is None:
                return
            for arg in agreements.agreements:
                yield GameCategoryAgreement.from_schema(
                    arg, game_category=self.game_category, obtaining_type=self, client=self._client
                )
            if not agreements.page_info.has_next_page:
                return
            cursor = agreements.page_info.end_cursor

    async def get_agreements(
        self, *, count: int = 24, cursor: str | None = None
    ) -> list[GameCategoryAgreement]:
        remain = count
        resp = []
        while remain > 0:
            agreements = await self._client.raw.games.get_game_category_agreements(
                game_category_id=self.id,
                obtaining_type_id=self.id,
                user_id=self._client.id,
                cursor=cursor,
            )
            if agreements is None:
                break
            for arg in agreements.agreements:
                resp.append(
                    GameCategoryAgreement.from_schema(
                        arg,
                        game_category=self.game_category,
                        obtaining_type=self,
                        client=self._client,
                    )
                )
            if not agreements.page_info.has_next_page:
                break
            cursor = agreements.page_info.end_cursor
            remain -= min(24, remain)

        return resp


@dataclass(slots=True)
class GameCategory:
    id: str
    name: str
    slug: str

    game: "Game" = field(repr=False, default=None)
    _client: "Playerok" = field(repr=False, default=None)

    @classmethod
    def from_schema(
        cls, f: SchemaGameCategory, game: "Game" = None, client: "Playerok" = None
    ) -> "GameCategory":
        return cls(id=f.id, name=f.name, slug=f.slug, game=game, _client=client)

    async def iter_agreements(
        self,
        *,
        cursor: str | None = None,
    ) -> AsyncIterator[GameCategoryAgreement]:
        while True:
            agreements = await self._client.raw.games.get_game_category_agreements(
                game_category_id=self.id,
                user_id=self._client.id,
                cursor=cursor,
            )
            if agreements is None:
                return
            for arg in agreements.agreements:
                yield GameCategoryAgreement.from_schema(
                    arg, game_category=self, client=self._client
                )
            if not agreements.page_info.has_next_page:
                return
            cursor = agreements.page_info.end_cursor

    async def get_agreements(
        self, *, count: int = 24, cursor: str | None = None
    ) -> list[GameCategoryAgreement]:
        remain = count
        resp = []
        while remain > 0:
            agreements = await self._client.raw.games.get_game_category_agreements(
                game_category_id=self.id,
                user_id=self._client.id,
                cursor=cursor,
            )
            if agreements is None:
                break
            for arg in agreements.agreements:
                resp.append(
                    GameCategoryAgreement.from_schema(arg, game_category=self, client=self._client)
                )
            if not agreements.page_info.has_next_page:
                break
            cursor = agreements.page_info.end_cursor
            remain -= min(24, remain)

        return resp

    async def iter_obtaining_types(
        self,
        *,
        cursor: str | None = None,
    ) -> AsyncIterator[GameCategoryObtainingType]:
        while True:
            obtaining_types = await self._client.raw.games.get_game_category_obtaining_types(
                game_category_id=self.id,
                cursor=cursor,
            )
            if obtaining_types is None:
                return
            for arg in obtaining_types.obtaining_types:
                yield GameCategoryObtainingType.from_schema(
                    arg, game_category=self, client=self._client
                )
            if not obtaining_types.page_info.has_next_page:
                return
            cursor = obtaining_types.page_info.end_cursor

    async def get_obtaining_types(
        self, *, count: int = 24, cursor: str | None = None
    ) -> list[GameCategoryObtainingType]:
        remain = count
        resp = []
        while remain > 0:
            obtaining_types = await self._client.raw.games.get_game_category_obtaining_types(
                game_category_id=self.id,
                cursor=cursor,
            )
            if obtaining_types is None:
                break
            for arg in obtaining_types.obtaining_types:
                resp.append(
                    GameCategoryObtainingType.from_schema(
                        arg, game_category=self, client=self._client
                    )
                )
            if not obtaining_types.page_info.has_next_page:
                break
            cursor = obtaining_types.page_info.end_cursor
            remain -= min(24, remain)

        return resp

    async def get_options(self) -> list[GameCategoryOption]:
        options = {}
        raw_options = await self._client.raw.games.get_game_category_options(
            game_category_id=self.id
        )
        for option in raw_options:
            if option.field not in options:
                options[option.field] = GameCategoryOption(
                    option.id,
                    type=option.type,
                    group_name=option.group,
                    slug=option.field,
                    possible_values=[],
                )

            option_object = options[option.field]
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
            else:
                raise TypeError(f"Unknown option type: {option.type}")

        return list(options.values())


@dataclass(slots=True)
class Game:
    id: str
    name: str
    slug: str
    logo: File | None
    categories: list[GameCategory]
    type: GameType = GameType.GAME

    _client: "Playerok" = field(repr=False, default=None)

    @classmethod
    def from_schema(cls, f: SchemaGame, client: "Playerok" = None) -> "Game":
        game = cls(
            id=f.id,
            name=f.name,
            categories=[],
            type=f.type,
            slug=f.slug,
            logo=File.from_schema(f.logo) if f.logo else None,
            _client=client,
        )

        for category in f.categories:
            game.categories.append(GameCategory.from_schema(category, game=game, client=client))

        return game
