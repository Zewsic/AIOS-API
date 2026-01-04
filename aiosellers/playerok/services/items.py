from ..core import PlayerokClient, _dig, _raise_on_gql_errors
from ..graphql import GraphQLQuery as GQL
from ..models import Item, ItemList, ItemsSortOptions


class ItemsService(PlayerokClient):
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

        response = await self.request(
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

        response = await self.request("post", "graphql", GQL.get_item(id=id, slug=slug))
        raw = response.json()
        _raise_on_gql_errors(raw)

        data = _dig(raw, ("data", "item"))
        if data is None:
            return None

        return Item(**data)
