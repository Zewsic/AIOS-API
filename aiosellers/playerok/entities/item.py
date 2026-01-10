from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..schemas.enums import ItemStatuses, PriorityTypes

if TYPE_CHECKING:  # pragma: no cover
    from ..playerok import Playerok
    from .game import Game, GameCategory
    from .user import User


@dataclass(slots=True)
class Item:
    id: str
    slug: str | None = None
    name: str | None = None
    description: str | None = None
    price: int | None = None
    status: ItemStatuses | None = None
    priority: PriorityTypes | None = None

    game_id: str | None = None
    category_id: str | None = None
    obtaining_type_id: str | None = None
    user_id: str | None = None

    _client: Playerok | None = field(default=None, repr=False, init=False, compare=False)

    def _require_client(self) -> Playerok:
        if self._client is None:
            raise RuntimeError(
                f"{self.__class__.__name__} is not attached to a client. "
                f"Use client.items.get() to fetch an active instance."
            )
        return self._client

    async def refresh(self) -> Item:
        return await self._require_client().items.get(self.id, force_refresh=True)

    async def get_category(self) -> GameCategory | None:
        if not self.category_id:
            return None
        game = await self.get_game()
        if not game:
            return None
        for cat in game.categories:
            if cat.id == self.category_id:
                return cat
        return None

    async def get_user(self) -> User | None:
        if not self.user_id:
            return None
        return await self._require_client().account.get_user(self.user_id)

    async def get_game(self) -> Game | None:
        if not self.game_id:
            return None
        return await self._require_client().games.get(id=self.game_id)

    async def get_deals(self, limit: int = 24) -> list:
        from .deal import Deal  # noqa: F401

        return await self._require_client().deals.list(
            limit=limit,
            item_id=self.id,
        )

    async def get_obtaining_fields(self) -> list:
        """Get OBTAINING_DATA fields for buying this item.

        These are fields that buyer needs to fill when creating a deal
        (e.g. game login, nickname, etc.)

        Returns:
            List of GameCategoryDataField with type OBTAINING_DATA
        """
        from ..schemas.enums import GameCategoryDataFieldTypes

        if not self.category_id:
            raise ValueError("Item has no category_id")
        if not self.obtaining_type_id:
            raise ValueError("Item has no obtaining_type_id")

        # Explicitly request OBTAINING_DATA type fields (for buyer)
        return await self._require_client().games.get_data_fields(
            self.category_id,
            self.obtaining_type_id,
            type=GameCategoryDataFieldTypes.OBTAINING_DATA,
        )

    async def create_deal(
        self,
        *,
        obtaining_fields: dict[str, str] | list | None = None,
        comment: str | None = None,
    ):
        """Create a deal to buy this item.

        Example:
            # Get fields and fill them
            fields = await item.get_obtaining_fields()
            fields[0].set_value("my_login")
            fields[1].set_value("my_password")

            # Create deal
            deal = await item.create_deal(obtaining_fields=fields, comment="Fast please!")
        """
        return await self._require_client().deals.create(
            self,
            obtaining_fields=obtaining_fields,
            comment=comment,
        )


@dataclass(slots=True)
class MyItem(Item):
    prev_price: int | None = None
    priority_price: int | None = None
    priority_position: int | None = None
    is_editable: bool | None = None
    buyer: object | None = None  # UserProfile | None

    async def update(
        self,
        *,
        name: str | None = None,
        price: int | None = None,
        description: str | None = None,
        options: dict[str, str] | list | None = None,
        data_fields: dict[str, str] | list | None = None,
        remove_attachments: list[str] | None = None,
        add_attachments: list[str] | None = None,
    ) -> MyItem:
        return await self._require_client().items.update(
            self.id,
            name=name,
            price=price,
            description=description,
            options=options,
            data_fields=data_fields,
            remove_attachments=remove_attachments,
            add_attachments=add_attachments,
        )

    async def remove(self) -> bool:
        return await self._require_client().items.remove(self.id)

    async def publish(self, *, premium: bool = False) -> MyItem:
        return await self._require_client().items.publish(self.id, premium=premium)

    async def set_normal_priority(self) -> MyItem:
        return await self._require_client().items.set_normal_priority(self.id)

    async def set_premium_priority(self) -> MyItem:
        return await self._require_client().items.set_premium_priority(self.id)
