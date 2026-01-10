"""Deals API module."""

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

from ..entities.deal import Deal
from ..schemas.enums import ItemDealDirections, ItemDealStatuses

if TYPE_CHECKING:
    from ..playerok import Playerok


class DealAPI:
    """Deal-related API methods."""

    def __init__(self, client: Playerok) -> None:
        self._client = client

    def _create_deal(self, schema) -> Deal:
        """Create Deal entity from schema and attach client."""
        deal = Deal(
            id=schema.id,
            status=schema.status,
            user_id=schema.user.id if schema.user else None,
            chat_id=schema.chat.id if schema.chat else None,
        )
        deal._client = self._client

        if self._client._use_identity_map:
            self._client._identity_maps.deals.set(schema.id, deal)

        return deal

    async def get(self, deal_id: str, *, force_refresh: bool = False) -> Deal | None:
        """Get deal by ID.

        Args:
            deal_id: Deal ID to fetch.
            force_refresh: If True, bypass identity map and fetch fresh data.

        Returns:
            Deal entity with client attached, or None if not found.
        """
        # Check identity map first
        if not force_refresh and self._client._use_identity_map:
            cached = self._client._identity_maps.deals.get(deal_id)
            if cached:
                return cached

        # Fetch from API
        schema = await self._client._raw.deals.get_deal(deal_id)
        if schema is None:
            return None

        return self._create_deal(schema)

    async def list(
        self,
        *,
        limit: int = 24,
        cursor: str | None = None,
        statuses: list[ItemDealStatuses] | None = None,
        direction: ItemDealDirections | None = None,
        user_id: str | None = None,
    ) -> list[Deal]:
        """Get list of deals.

        Args:
            limit: Maximum number of deals to fetch.
            cursor: Pagination cursor.
            statuses: Filter by deal statuses.
            direction: Filter by deal direction (IN/OUT).
            user_id: Filter results by user ID.

        Returns:
            List of Deal entities.
        """
        result = []
        remain = limit
        current_cursor = cursor

        while remain > 0:
            response = await self._client._raw.deals.get_deals(
                user_id=self._client._me_id,
                count=min(24, remain),
                after_cursor=current_cursor,
                statuses=statuses,
                direction=direction,
            )
            if response is None or not response.deals:
                break

            for schema in response.deals:
                deal_user_id = schema.user.id if schema.user else None

                # Filter by user_id if specified
                if user_id is not None and deal_user_id != user_id:
                    continue

                result.append(self._create_deal(schema))
                if len(result) >= limit:
                    break

            if len(result) >= limit:
                break

            remain -= len(response.deals)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

        return result[:limit]

    async def iter(
        self,
        *,
        cursor: str | None = None,
        statuses: list[ItemDealStatuses] | None = None,
        direction: ItemDealDirections | None = None,
        user_id: str | None = None,
    ) -> AsyncIterator[Deal]:
        """Iterate over all deals.

        Args:
            cursor: Starting pagination cursor.
            statuses: Filter by deal statuses.
            direction: Filter by deal direction (IN/OUT).
            user_id: Filter results by user ID.

        Yields:
            Deal entities.
        """
        current_cursor = cursor

        while True:
            response = await self._client._raw.deals.get_deals(
                user_id=self._client._me_id,
                after_cursor=current_cursor,
                statuses=statuses,
                direction=direction,
            )
            if response is None or not response.deals:
                return

            for schema in response.deals:
                deal_user_id = schema.user.id if schema.user else None

                # Filter by user_id if specified
                if user_id is not None and deal_user_id != user_id:
                    continue

                yield self._create_deal(schema)

            if not response.page_info.has_next_page:
                break
            current_cursor = response.page_info.end_cursor

    async def confirm(self, deal_id: str) -> Deal:
        """Confirm a deal.

        Args:
            deal_id: Deal ID to confirm.

        Returns:
            Updated Deal entity.
        """
        updated = await self._client._raw.deals.update_deal(deal_id, ItemDealStatuses.CONFIRMED)
        if updated is None:
            # Fallback: refetch
            return await self.get(deal_id, force_refresh=True)
        return self._create_deal(updated)

    async def complete(self, deal_id: str) -> Deal:
        """Complete a deal.

        Args:
            deal_id: Deal ID to confirm.

        Returns:
            Updated Deal entity.
        """
        updated = await self._client._raw.deals.update_deal(deal_id, ItemDealStatuses.SENT)
        if updated is None:
            # Fallback: refetch
            return await self.get(deal_id, force_refresh=True)
        return self._create_deal(updated)

    async def cancel(self, deal_id: str) -> Deal:
        """Cancel a deal.

        Args:
            deal_id: Deal ID to cancel.

        Returns:
            Updated Deal entity.
        """
        updated = await self._client._raw.deals.update_deal(deal_id, ItemDealStatuses.ROLLED_BACK)
        if updated is None:
            return await self.get(deal_id, force_refresh=True)
        return self._create_deal(updated)
