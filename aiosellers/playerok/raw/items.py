from __future__ import annotations

from ..core.utils import _dig, _raise_on_gql_errors
from ..graphql import GraphQLQuery as GQL
from ..schemas import (
    Item,
    ItemList,
    ItemPriorityStatus,
    ItemsSortOptions,
    MyItem,
    TransactionPaymentMethodIds,
    TransactionProviderIds,
)
from ..transport import PlayerokTransport


class RawItemsService:
    def __init__(self, transport: PlayerokTransport):
        self._transport = transport

    async def get_items(
        self,
        count: int = 24,
        cursor: str | None = None,
        game_id: str | None = None,
        category_id: str | None = None,
        minimal_price: int | None = None,
        maximal_price: int | None = None,
        has_discount: bool | None = None,
        has_reviews: bool | None = None,
        attributes: list[dict[str, str]] | None = None,
        search: str | None = None,
        sort: ItemsSortOptions | None = None,
    ) -> ItemList | None:
        if game_id is None or category_id is None:
            raise ValueError("Can't get items without game_id and category_id")

        response = await self._transport.request(
            "post",
            "graphql",
            GQL.get_items(
                count=count,
                cursor=cursor,
                game_id=game_id,
                category_id=category_id,
                minimal_price=minimal_price,
                maximal_price=maximal_price,
                has_discount=has_discount,
                has_reviews=has_reviews,
                attributes=attributes,
                search=search,
                sort=sort,
            ),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "items"))
        if data is None:
            return None
        return ItemList(**data)

    async def get_item(self, id: str | None = None, slug: str | None = None) -> Item | None:
        if id is None and slug is None:
            raise ValueError("Can't get item without id or slug")

        response = await self._transport.request("post", "graphql", GQL.get_item(id=id, slug=slug))
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "item"))
        if data is None:
            return None
        return Item(**data)

    async def create_item(
        self,
        game_category_id: str,
        obtaining_type_id: str,
        name: str,
        price: int,
        description: str,
        options: dict[str, str],
        data_fields: dict[str, str],
        attachments: list[str],
    ) -> MyItem | None:
        payload_data_fields = [{"fieldId": k, "value": v} for k, v in data_fields.items()]

        payload = GQL.create_item(
            game_category_id=game_category_id,
            obtaining_type_id=obtaining_type_id,
            name=name,
            price=int(price),
            description=description,
            attributes=options,
            data_fields=payload_data_fields,
            attachments_count=len(attachments),
        )

        files = {str(i + 1): open(attachments[i], "rb") for i in range(len(attachments))}
        try:
            response = await self._transport.request("post", "graphql", payload, files=files)
        finally:
            for f in files.values():
                f.close()

        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "createItem"))
        if data is None:
            return None
        return MyItem(**data)

    async def update_item(
        self,
        id: str,
        name: str | None = None,
        price: int | None = None,
        description: str | None = None,
        options: dict[str, str] | None = None,
        data_fields: dict[str, str] | None = None,
        remove_attachments: list[str] | None = None,
        add_attachments: list[str] | None = None,
    ) -> MyItem | None:
        payload_data_fields = (
            [{"fieldId": k, "value": v} for k, v in data_fields.items()]
            if data_fields is not None
            else None
        )

        payload = GQL.update_item(
            id=id,
            name=name,
            price=int(price) if price is not None else None,
            description=description,
            attributes=options,
            data_fields=payload_data_fields,
            removed_attachments=remove_attachments,
            attachments_count=len(add_attachments) if add_attachments else 0,
        )

        files = (
            {str(i + 1): open(add_attachments[i], "rb") for i in range(len(add_attachments))}
            if add_attachments
            else None
        )

        try:
            response = await self._transport.request("post", "graphql", payload, files=files)
        finally:
            if files:
                for f in files.values():
                    f.close()

        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "updateItem"))
        if data is None:
            return None
        return MyItem(**data)

    async def remove_item(self, id: str) -> bool:
        response = await self._transport.request("post", "graphql", GQL.remove_item(id=id))
        raw = response.json()
        _raise_on_gql_errors(raw)
        return True

    async def publish_item(
        self,
        item_id: str,
        priority_status_id: str,
        transaction_provider_id: TransactionProviderIds = TransactionProviderIds.LOCAL,
    ) -> MyItem | None:
        response = await self._transport.request(
            "post",
            "graphql",
            GQL.publish_item(
                item_id=item_id,
                priority_status_id=priority_status_id,
                transaction_provider_id=transaction_provider_id.name,
            ),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "publishItem"))
        if data is None:
            return None
        return MyItem(**data)

    async def get_item_priority_statuses(
        self, item_id: str, price: int
    ) -> list[ItemPriorityStatus]:
        response = await self._transport.request(
            "post", "graphql", GQL.get_item_priority_statuses(item_id=item_id, price=price)
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "itemPriorityStatuses")) or []
        return [ItemPriorityStatus(**status) for status in data]

    async def increase_item_priority_status(
        self,
        item_id: str,
        priority_status_id: str,
        payment_method_id: TransactionPaymentMethodIds | None = None,
        transaction_provider_id: TransactionProviderIds = TransactionProviderIds.LOCAL,
    ) -> MyItem | None:
        response = await self._transport.request(
            "post",
            "graphql",
            GQL.increase_item_priority_status(
                item_id=item_id,
                priority_status_id=priority_status_id,
                payment_method_id=payment_method_id.name if payment_method_id else None,
                transaction_provider_id=transaction_provider_id.name,
            ),
        )
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "increaseItemPriorityStatus"))
        if data is None:
            return None
        return MyItem(**data)
