"""Item entity."""

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
    """Item entity - represents a public item."""

    id: str
    slug: str | None = None
    name: str | None = None
    description: str | None = None
    price: int | None = None
    status: ItemStatuses | None = None
    priority: PriorityTypes | None = None

    game_id: str | None = None
    category_id: str | None = None
    user_id: str | None = None

    _client: Playerok | None = field(default=None, repr=False, init=False, compare=False)

    def _require_client(self) -> Playerok:
        """Ensure client is attached, raise error if not."""
        if self._client is None:
            raise RuntimeError(
                f"{self.__class__.__name__} is not attached to a client. "
                f"Use client.items.get() to fetch an active instance."
            )
        return self._client

    async def refresh(self) -> Item:
        """Refresh item data from server."""
        return await self._require_client().items.get(self.id, force_refresh=True)

    async def get_category(self) -> GameCategory | None:
        """Get category for this item."""
        if not self.category_id:
            return None
        # Get game first to find category
        game = await self.get_game()
        if not game:
            return None
        for cat in game.categories:
            if cat.id == self.category_id:
                return cat
        return None

    async def get_user(self) -> User | None:
        """Get user (seller) of this item."""
        if not self.user_id:
            return None
        return await self._require_client().account.get_user(self.user_id)

    async def get_game(self) -> Game | None:
        """Get game for this item."""
        if not self.game_id:
            return None
        return await self._require_client().games.get(id=self.game_id)

    async def get_deals(self, limit: int = 24) -> list:
        """Get all deals for this item.

        Returns:
            List of Deal entities.
        """
        # Import here to avoid circular imports
        from .deal import Deal  # noqa: F401

        return await self._require_client().deals.list(
            limit=limit,
        )


@dataclass(slots=True)
class MyItem(Item):
    """MyItem entity - represents a user's own item with extended fields."""

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
        """Update this item.

        Args:
            name: Item name.
            price: Item price.
            description: Item description.
            options: Options as dict or list of GameCategoryOption objects.
            data_fields: Data fields as dict or list of GameCategoryDataField objects.
            remove_attachments: List of attachment IDs to remove.
            add_attachments: List of file paths to add.

        Returns:
            Updated MyItem entity.
        """
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
        """Remove this item.

        Returns:
            True if removed successfully.
        """
        return await self._require_client().items.remove(self.id)

    async def publish(self, *, premium: bool = False) -> MyItem:
        """Publish this item.

        Args:
            premium: If True, publish with premium priority. Default is normal priority.

        Returns:
            Updated MyItem entity.
        """
        return await self._require_client().items.publish(self.id, premium=premium)

    async def set_normal_priority(self) -> MyItem:
        """Set normal (lowest) priority for this item.

        Returns:
            Updated MyItem entity.
        """
        return await self._require_client().items.set_normal_priority(self.id)

    async def set_premium_priority(self) -> MyItem:
        """Set premium (highest) priority for this item.

        Returns:
            Updated MyItem entity.

        Raises:
            ValueError: If premium priority is not available for this item's category.
        """
        return await self._require_client().items.set_premium_priority(self.id)
