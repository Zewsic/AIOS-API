from typing import Any

from .models import (
    GameCategoryDataFieldTypes,
    GameCategoryInstructionTypes,
    GameType,
    ItemsSortOptions,
    QueryID,
)


def _persisted(
    operation_name: str,
    variables: dict[str, Any],
    *,
    sha256_hash: Any | None = None,
    query: str | None = None,
) -> dict[str, Any]:
    r = {
        "operationName": operation_name,
        "variables": variables,
    }
    if query:
        r["query"] = query
    if sha256_hash:
        r["extensions"] = {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": sha256_hash,
            }
        }
    return r


class GraphQLQuery:
    @staticmethod
    def get_me():
        return _persisted(
            operation_name="viewer",
            variables={},
            query="query viewer {\n  viewer {\n    ...Viewer\n    __typename\n  }\n}\n\nfragment Viewer on User {\n  id\n  username\n  email\n  role\n  hasFrozenBalance\n  supportChatId\n  systemChatId\n  unreadChatsCounter\n  isBlocked\n  isBlockedFor\n  isFundsProtectionActive\n  createdAt\n  lastItemCreatedAt\n  hasConfirmedPhoneNumber\n  canPublishItems\n  chosenVerifiedCard {\n    ...MinimalUserBankCard\n    __typename\n  }\n  profile {\n    id\n    avatarURL\n    testimonialCounter\n    __typename\n  }\n  __typename\n}\n\nfragment MinimalUserBankCard on UserBankCard {\n  id\n  cardFirstSix\n  cardLastFour\n  cardType\n  isChosen\n  __typename\n}",
        )

    @staticmethod
    def get_user(username: str | None = None, id: str | None = None) -> dict[str, Any]:
        return _persisted(
            operation_name="user",
            variables={"id": id, "username": username, "hasSupportAccess": False},
            sha256_hash=QueryID.user.value,
        )

    @staticmethod
    def get_games(
        count: int = 24, type: GameType | None = None, cursor: str | None = None
    ) -> dict[str, Any]:
        return _persisted(
            operation_name="games",
            variables={
                "pagination": {"first": count, "after": cursor},
                "filter": {"type": type.name} if type else {},
            },
            sha256_hash=QueryID.games.value,
        )

    @staticmethod
    def get_game(id: str | None = None, slug: str | None = None) -> dict[str, Any]:
        return _persisted(
            operation_name="GamePage",
            variables={"id": id, "slug": slug},
            sha256_hash=QueryID.game.value,
        )

    @staticmethod
    def get_game_category(
        game_id: str | None = None,
        slug: str | None = None,
        id: str | None = None,
    ) -> dict[str, Any]:
        return _persisted(
            operation_name="GamePageCategory",
            variables={"id": id, "gameId": game_id, "slug": slug},
            sha256_hash=QueryID.game_category.value,
        )

    @staticmethod
    def get_game_category_agreements(
        game_category_id: str,
        user_id: str | None = None,
        count: int = 24,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        return _persisted(
            operation_name="gameCategoryAgreements",
            variables={
                "pagination": {"first": count, "after": cursor},
                "filter": {"gameCategoryId": game_category_id, "userId": user_id},
            },
            sha256_hash=QueryID.game_category_agreements.value,
        )

    @staticmethod
    def get_game_category_obtaining_types(
        game_category_id: str,
        count: int = 24,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        return _persisted(
            operation_name="gameCategoryObtainingTypes",
            variables={
                "pagination": {"first": count, "after": cursor},
                "filter": {"gameCategoryId": game_category_id},
            },
            sha256_hash=QueryID.game_category_obtaining_types.value,
        )

    @staticmethod
    def get_game_category_instructions(
        game_category_id: str,
        obtaining_type_id: str,
        count: int = 24,
        type: GameCategoryInstructionTypes | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        return _persisted(
            operation_name="gameCategoryInstructions",
            variables={
                "pagination": {"first": count, "after": cursor},
                "filter": {
                    "gameCategoryId": game_category_id,
                    "obtainingTypeId": obtaining_type_id,
                    "type": type.name if type else None,
                },
            },
            sha256_hash=QueryID.game_category_instructions.value,
        )

    @staticmethod
    def get_game_category_data_fields(
        game_category_id: str,
        obtaining_type_id: str,
        count: int = 24,
        type: GameCategoryDataFieldTypes | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        return _persisted(
            operation_name="gameCategoryDataFields",
            variables={
                "pagination": {"first": count, "after": cursor},
                "filter": {
                    "gameCategoryId": game_category_id,
                    "obtainingTypeId": obtaining_type_id,
                    "type": type.name if type else None,
                },
            },
            sha256_hash=QueryID.game_category_data_fields.value,
        )

    @staticmethod
    def get_items(
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
    ) -> dict[str, Any]:
        filters = {
            "gameId": game_id,
            "gameCategoryId": category_id,
            "status": ["APPROVED"],
        }
        sort_field = None

        if minimal_price or maximal_price:
            filters["price"] = {"min": minimal_price, "max": maximal_price}
        if has_discount:
            filters["hasDiscount"] = has_discount
        if has_reviews:
            filters["hasTestimonials"] = has_reviews
        if attributes:
            filters["attributes"] = attributes
        if search:
            filters["searchQuery"] = search
        if sort:
            if "PRICE" in sort:
                field = "price"
            else:
                field = "userRating"
            if "ASC" in sort:
                direction = "ASC"
            else:
                direction = "DESC"

            sort_field = {"field": field, "direction": direction}

        return _persisted(
            operation_name="items",
            variables={
                "pagination": {"first": count, "after": cursor},
                "filter": filters,
                "sort": sort_field,
            },
            sha256_hash=QueryID.items.value,
        )

    @staticmethod
    def get_item(id: str | None = None, slug: str | None = None) -> dict[str, Any]:
        return _persisted(
            operation_name="item",
            variables={
                "id": id,
                "slug": slug,
                "hasSupportAccess": False,
                "showForbiddenImage": True,
            },
            sha256_hash=QueryID.item.value,
        )
