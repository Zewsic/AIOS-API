"""Items API module."""

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

from ..entities.game import GameCategoryDataField, GameCategoryOption
from ..entities.item import Item, MyItem
from ..schemas.items import Item as ItemSchema
from ..schemas.items import MyItem as MyItemSchema

if TYPE_CHECKING:
    from ..playerok import Playerok


class ItemAPI:
    """Item-related API methods."""

    def __init__(self, client: Playerok) -> None:
        self._client = client

    def _create_item(self, schema) -> Item:
        """Create Item entity from schema and attach client."""
        # Check identity map first if ID is available
        if self._client._use_identity_map and hasattr(schema, "id"):
            cached = self._client._identity_maps.items.get(schema.id)
            if cached:
                return cached

        item = Item(
            id=schema.id,
            slug=schema.slug,
            name=schema.name,
            description=schema.description,
            price=schema.price,
            status=schema.status,
            priority=schema.priority,
            game_id=getattr(schema, "game_id", None),
            category_id=getattr(schema, "category_id", None),
            user_id=schema.user.id if schema.user else None,
        )
        item._client = self._client

        # Store in identity map
        if self._client._use_identity_map:
            self._client._identity_maps.items.set(item.id, item)

        return item

    def _create_my_item(self, schema) -> MyItem:
        """Create MyItem entity from schema and attach client."""
        # Check identity map first if ID is available
        if self._client._use_identity_map and hasattr(schema, "id"):
            cached = self._client._identity_maps.items.get(schema.id)
            if cached:
                return cached

        if type(schema) is ItemSchema:
            item = MyItem(
                id=schema.id,
                slug=schema.slug,
                name=schema.name,
                description=schema.description,
                price=schema.price,
                prev_price=schema.raw_price,
                status=schema.status,
                priority=schema.priority,
                priority_position=schema.priority_position,
                game_id=getattr(schema, "game_id", None),
                category_id=getattr(schema, "category_id", None),
                user_id=schema.user.id if schema.user else None,
            )
        elif type(schema) is MyItemSchema:
            item = MyItem(
                id=schema.id,
                slug=schema.slug,
                name=schema.name,
                description=schema.description,
                price=schema.price,
                status=schema.status,
                priority=schema.priority,
                game_id=getattr(schema, "game_id", None),
                category_id=getattr(schema, "category_id", None),
                user_id=schema.user.id if schema.user else None,
                prev_price=schema.prev_price,
                priority_price=schema.priority_price,
                priority_position=schema.priority_position,
                is_editable=schema.is_editable,
                buyer=schema.buyer,
            )

            # Store in identity map
            if self._client._use_identity_map:
                self._client._identity_maps.items.set(item.id, item)

        item._client = self._client
        return item

    def _extract_options(
        self, options: dict[str, str] | list[GameCategoryOption] | None
    ) -> dict[str, str] | None:
        """Extract options as dict from list of objects or return dict as is."""
        if options is None:
            return None
        if isinstance(options, dict):
            return options
        # List of GameCategoryOption objects
        result = {}
        for opt in options:
            if hasattr(opt, "_input_value") and opt._input_value is not None:
                result[opt.slug] = str(opt._input_value)
        return result if result else None

    def _extract_data_fields(
        self, data_fields: dict[str, str] | list[GameCategoryDataField] | None
    ) -> dict[str, str] | None:
        """Extract data_fields as dict from list of objects or return dict as is."""
        if data_fields is None:
            return None
        if isinstance(data_fields, dict):
            return data_fields
        # List of GameCategoryDataField objects
        result = {}
        for field in data_fields:
            if hasattr(field, "_input_value") and field._input_value is not None:
                result[field.id] = field._input_value
        return result if result else None

    async def _get_priority_statuses(self, item_id: str, price: int):
        """Get available priority statuses for an item (internal method)."""
        return await self._client._raw.items.get_item_priority_statuses(item_id, price)

    async def get(
        self, id: str | None = None, *, slug: str | None = None, force_refresh: bool = False
    ) -> Item | None:
        """Get item by ID or slug.

        Args:
            id: Item ID to fetch.
            slug: Item slug to fetch.
            force_refresh: If True, bypass identity map and fetch fresh data.

        Returns:
            Item entity with client attached, or None if not found.
        """
        # Check identity map first (only by ID)
        if id and not force_refresh and self._client._use_identity_map:
            cached = self._client._identity_maps.items.get(id)
            if cached:
                return cached

        # Fetch from API
        schema = await self._client._raw.items.get_item(id, slug)
        if schema is None:
            return None

        return self._create_item(schema)

    async def list(
        self,
        *,
        limit: int = 24,
        cursor: str | None = None,
        game_id: str | None = None,
        category_id: str | None = None,
        user_id: str | None = None,
        minimal_price: int | None = None,
        maximal_price: int | None = None,
        has_discount: bool | None = None,
        has_reviews: bool | None = None,
        attributes: list[dict[str, str]] | None = None,
        search: str | None = None,
    ) -> list[Item]:
        """Get list of items with filters.

        Args:
            limit: Maximum number of items to fetch.
            cursor: Pagination cursor.
            game_id: Filter by game ID.
            category_id: Filter by category ID.
            user_id: Filter by user ID.
            minimal_price: Minimum price.
            maximal_price: Maximum price.
            has_discount: Filter by discount.
            has_reviews: Filter by reviews.
            attributes: Filter by attributes.
            search: Search query.

        Returns:
            List of Item entities.
        """
        result = []
        remain = limit
        current_cursor = cursor

        while remain > 0:
            response = await self._client._raw.items.get_items(
                count=min(24, remain),
                cursor=current_cursor,
                game_id=game_id,
                user_id=user_id,
                category_id=category_id,
                minimal_price=minimal_price,
                maximal_price=maximal_price,
                has_discount=has_discount,
                has_reviews=has_reviews,
                attributes=attributes,
                search=search,
            )
            if response is None or not response.items:
                break

            for schema in response.items:
                result.append(self._create_item(schema))

            remain -= len(response.items)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

        return result[:limit]

    async def iter(
        self,
        *,
        cursor: str | None = None,
        game_id: str | None = None,
        category_id: str | None = None,
        user_id: str | None = None,
        minimal_price: int | None = None,
        maximal_price: int | None = None,
        has_discount: bool | None = None,
        has_reviews: bool | None = None,
        attributes: list[dict[str, str]] | None = None,
        search: str | None = None,
    ) -> AsyncIterator[Item]:
        """Iterate over all items.

        Args:
            cursor: Starting pagination cursor.
            game_id: Filter by game ID.
            category_id: Filter by category ID.
            user_id: Filter by user ID.
            minimal_price: Minimum price.
            maximal_price: Maximum price.
            has_discount: Filter by discount.
            has_reviews: Filter by reviews.
            attributes: Filter by attributes.
            search: Search query.

        Yields:
            Item entities.
        """
        current_cursor = cursor

        while True:
            response = await self._client._raw.items.get_items(
                cursor=current_cursor,
                game_id=game_id,
                user_id=user_id,
                category_id=category_id,
                minimal_price=minimal_price,
                maximal_price=maximal_price,
                has_discount=has_discount,
                has_reviews=has_reviews,
                attributes=attributes,
                search=search,
            )
            if response is None or not response.items:
                return

            for schema in response.items:
                yield self._create_item(schema)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

    async def list_self(self, *, limit: int = 24, cursor: str | None = None) -> list[MyItem]:
        """Get list of own items.

        Args:
            limit: Maximum number of items to fetch.
            cursor: Pagination cursor.

        Returns:
            List of MyItem entities.
        """
        result = []
        remain = limit
        current_cursor = cursor

        while remain > 0:
            response = await self._client._raw.items.get_items(
                count=min(24, remain),
                cursor=current_cursor,
                user_id=self._client._me_id,
            )
            if response is None or not response.items:
                break

            for schema in response.items:
                result.append(self._create_my_item(schema))

            remain -= len(response.items)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

        return result[:limit]

    async def iter_self(self, *, cursor: str | None = None) -> AsyncIterator[MyItem]:
        """Iterate over all own items.

        Args:
            cursor: Starting pagination cursor.

        Yields:
            MyItem entities.
        """
        current_cursor = cursor

        while True:
            response = await self._client._raw.items.get_items(
                cursor=current_cursor,
                user_id=self._client._me_id,
            )
            if response is None or not response.items:
                return

            for schema in response.items:
                yield self._create_my_item(schema)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

    async def create(
        self,
        *,
        category: str | object,
        obtaining_type: str | object,
        name: str,
        price: int,
        description: str,
        options: dict[str, str] | list[GameCategoryOption] | None = None,
        data_fields: dict[str, str] | list[GameCategoryDataField] | None = None,
        attachments: list[str] | None = None,
    ) -> MyItem | None:
        """Create a new item.

        Args:
            category: GameCategory entity or category ID string.
            obtaining_type: GameCategoryObtainingType entity or obtaining type ID string.
            name: Item name.
            price: Item price.
            description: Item description.
            options: Options as dict or list of GameCategoryOption objects.
            data_fields: Data fields as dict or list of GameCategoryDataField objects.
            attachments: List of file paths to attach.

        Returns:
            Created MyItem entity, or None if creation failed.
        """
        # Extract category ID (support both object and string)
        category_id = category.id if hasattr(category, "id") else category
        # Extract obtaining_type ID (support both object and string)
        obtaining_type_id = obtaining_type.id if hasattr(obtaining_type, "id") else obtaining_type

        # Extract options and data_fields
        options_dict = self._extract_options(options)
        data_fields_dict = self._extract_data_fields(data_fields)

        schema = await self._client._raw.items.create_item(
            game_category_id=category_id,
            obtaining_type_id=obtaining_type_id,
            name=name,
            price=price,
            description=description,
            options=options_dict or {},
            data_fields=data_fields_dict or {},
            attachments=attachments or [],
        )
        if schema is None:
            return None

        return self._create_my_item(schema)

    async def update(
        self,
        item_id: str,
        *,
        name: str | None = None,
        price: int | None = None,
        description: str | None = None,
        options: dict[str, str] | list[GameCategoryOption] | None = None,
        data_fields: dict[str, str] | list[GameCategoryDataField] | None = None,
        remove_attachments: list[str] | None = None,
        add_attachments: list[str] | None = None,
    ) -> MyItem | None:
        """Update an existing item.

        Args:
            item_id: Item ID to update.
            name: New item name.
            price: New item price.
            description: New item description.
            options: Options as dict or list of GameCategoryOption objects.
            data_fields: Data fields as dict or list of GameCategoryDataField objects.
            remove_attachments: List of attachment IDs to remove.
            add_attachments: List of file paths to add.

        Returns:
            Updated MyItem entity, or None if update failed.
        """
        # Extract options and data_fields
        options_dict = self._extract_options(options)
        data_fields_dict = self._extract_data_fields(data_fields)

        schema = await self._client._raw.items.update_item(
            id=item_id,
            name=name,
            price=price,
            description=description,
            options=options_dict,
            data_fields=data_fields_dict,
            remove_attachments=remove_attachments,
            add_attachments=add_attachments,
        )
        if schema is None:
            return None

        return self._create_my_item(schema)

    async def remove(self, item_id: str) -> bool:
        """Remove an item.

        Args:
            item_id: Item ID to remove.

        Returns:
            True if removed successfully.
        """
        return await self._client._raw.items.remove_item(item_id)

    async def publish(self, item_id: str, *, premium: bool = False) -> MyItem | None:
        """Publish an item with specified priority.

        Args:
            item_id: Item ID to publish.
            premium: If True, publish with premium priority. Default is normal priority.

        Returns:
            Updated MyItem entity, or None if publish failed.
        """
        # Get item to get price
        item = await self.get(item_id)
        if item is None or item.price is None:
            raise ValueError(f"Item {item_id} not found or price is missing")

        # Get available priority statuses
        statuses = await self._get_priority_statuses(item_id, item.price)

        # Find the appropriate priority status
        if premium:
            # Premium = first priority (index 0)
            if not statuses:
                raise ValueError("No premium priority available for this item")
            priority_status = statuses[0]
        else:
            # Normal = last priority (index -1)
            if not statuses:
                raise ValueError("No normal priority available for this item")
            priority_status = statuses[-1]

        schema = await self._client._raw.items.publish_item(
            item_id=item_id,
            priority_status_id=priority_status.id,
        )
        if schema is None:
            return None

        return self._create_my_item(schema)

    async def set_normal_priority(self, item_id: str) -> MyItem | None:
        """Set normal (lowest) priority for an item.

        Args:
            item_id: Item ID.

        Returns:
            Updated MyItem entity, or None if update failed.

        Raises:
            ValueError: If item not found or normal priority not available.
        """
        # Get item to get price
        item = await self.get(item_id)
        if item is None or item.price is None:
            raise ValueError(f"Item {item_id} not found or price is missing")

        # Get available priority statuses
        statuses = await self._get_priority_statuses(item_id, item.price)

        # Normal = last priority (index -1)
        if not statuses:
            raise ValueError("No normal priority available for this item")
        priority_status = statuses[-1]

        schema = await self._client._raw.items.increase_item_priority_status(
            item_id=item_id,
            priority_status_id=priority_status.id,
        )
        if schema is None:
            return None

        return self._create_my_item(schema)

    async def set_premium_priority(self, item_id: str) -> MyItem | None:
        """Set premium (highest) priority for an item.

        Args:
            item_id: Item ID.

        Returns:
            Updated MyItem entity, or None if update failed.

        Raises:
            ValueError: If item not found or premium priority not available.
        """
        # Get item to get price
        item = await self.get(item_id)
        if item is None or item.price is None:
            raise ValueError(f"Item {item_id} not found or price is missing")

        # Get available priority statuses
        statuses = await self._get_priority_statuses(item_id, item.price)

        # Premium = first priority (index 0)
        if not statuses:
            raise ValueError("No premium priority available for this item")
        priority_status = statuses[0]

        schema = await self._client._raw.items.increase_item_priority_status(
            item_id=item_id,
            priority_status_id=priority_status.id,
        )
        if schema is None:
            return None

        return self._create_my_item(schema)
