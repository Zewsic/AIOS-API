from datetime import datetime

from pydantic import Field, model_validator

from . import ApiModel, ItemStatuses, PageInfo, PriorityTypes, UserType
from .account import UserProfile
from .basic import File


class Item(ApiModel):
    id: str = Field(..., alias="id")
    slug: str = Field(..., alias="slug")
    name: str = Field(..., alias="name")
    price: int = Field(..., alias="price")
    raw_price: int = Field(..., alias="rawPrice")

    priority: PriorityTypes | None = Field(None, alias="priority")
    status: ItemStatuses | None = Field(None, alias="status")
    seller_type: UserType | None = Field(None, alias="sellerType")

    attachment: File | None = Field(None, alias="attachment")
    user: UserProfile | None = Field(None, alias="user")

    approval_date: datetime | None = Field(None, alias="approvalDate")
    priority_position: int | None = Field(None, alias="priorityPosition")
    views_counter: int | None = Field(None, alias="viewsCounter")
    fee_multiplier: float | None = Field(None, alias="feeMultiplier")
    created_at: datetime | None = Field(None, alias="createdAt")


class ItemList(ApiModel):
    items: list[Item] = Field(..., alias="items")
    page_info: PageInfo = Field(..., alias="pageInfo")
    total_count: int = Field(..., alias="totalCount")

    @model_validator(mode="before")
    @classmethod
    def _inflate_from_edges(cls, data):
        if not isinstance(data, dict):
            return data

        if "items" not in data:
            edges = data.get("edges") or []
            data["items"] = [(edge or {}).get("node") for edge in edges if (edge or {}).get("node")]

        return data
