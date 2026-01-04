from datetime import datetime
from typing import Optional, List

from pydantic import Field, model_validator

from . import (
    ApiModel,
    PageInfo,
    GameCategoryDataFieldTypes,
    GameCategoryDataFieldInputTypes,
    GameCategoryOptionTypes,
    GameCategoryAgreementIconTypes,
    GameCategoryAutoConfirmPeriods,
    GameType,
)
from .basic import File


class GameCategoryDataField(ApiModel):
    id: str = Field(..., alias="id")
    label: str = Field(..., alias="label")

    type: GameCategoryDataFieldTypes = Field(..., alias="type")
    input_type: GameCategoryDataFieldInputTypes = Field(..., alias="inputType")

    copyable: bool = Field(..., alias="copyable")
    hidden: bool = Field(..., alias="hidden")
    required: bool = Field(..., alias="required")

    value: Optional[str] = Field(None, alias="value")


class GameCategoryDataFieldList(ApiModel):
    data_fields: List[GameCategoryDataField] = Field(..., alias="dataFields")
    page_info: PageInfo = Field(..., alias="pageInfo")
    total_count: int = Field(..., alias="totalCount")

    @model_validator(mode="before")
    @classmethod
    def _inflate_from_edges(cls, data):
        if not isinstance(data, dict):
            return data

        if "dataFields" not in data and "data_fields" not in data:
            edges = data.get("edges") or []
            data["dataFields"] = [
                (edge or {}).get("node") for edge in edges if (edge or {}).get("node")
            ]

        if "data_fields" in data and "dataFields" not in data:
            data["dataFields"] = data["data_fields"]

        return data


class GameCategoryProps(ApiModel):
    min_reviews: int = Field(..., alias="minTestimonials")
    min_reviews_for_seller: int = Field(..., alias="minTestimonialsForSeller")


class GameCategoryOption(ApiModel):
    id: str = Field(..., alias="id")
    group: str = Field(..., alias="group")
    label: str = Field(..., alias="label")

    type: GameCategoryOptionTypes = Field(..., alias="type")
    field: str = Field(..., alias="field")
    value: str = Field(..., alias="value")
    value_range_limit: Optional[int] = Field(None, alias="valueRangeLimit")


class GameCategoryAgreement(ApiModel):
    id: str = Field(..., alias="id")
    description: str = Field(..., alias="description")
    icon_type: GameCategoryAgreementIconTypes = Field(..., alias="iconType")
    sequence: int = Field(..., alias="sequence")


class GameCategoryAgreementList(ApiModel):
    agreements: List[GameCategoryAgreement] = Field(..., alias="agreements")
    page_info: PageInfo = Field(..., alias="pageInfo")
    total_count: int = Field(..., alias="totalCount")

    @model_validator(mode="before")
    @classmethod
    def _inflate_from_edges(cls, data):
        if not isinstance(data, dict):
            return data

        if "agreements" not in data:
            edges = data.get("edges") or []
            data["agreements"] = [
                (edge or {}).get("node") for edge in edges if (edge or {}).get("node")
            ]
        return data


class GameCategoryObtainingType(ApiModel):
    id: str = Field(..., alias="id")
    name: str = Field(..., alias="name")
    description: str = Field(..., alias="description")

    game_category_id: str = Field(..., alias="gameCategoryId")
    no_comment_from_buyer: bool = Field(..., alias="noCommentFromBuyer")
    instruction_for_buyer: Optional[str] = Field(None, alias="instructionForBuyer")
    instruction_for_seller: Optional[str] = Field(None, alias="instructionForSeller")

    sequence: int = Field(..., alias="sequence")
    fee_multiplier: Optional[float] = Field(None, alias="feeMultiplier")

    agreements: List[GameCategoryAgreement] = Field(..., alias="agreements")
    props: Optional[GameCategoryProps] = Field(None, alias="props")


class GameCategoryObtainingTypeList(ApiModel):
    obtaining_types: List[GameCategoryObtainingType] = Field(
        ..., alias="obtainingTypes"
    )
    page_info: PageInfo = Field(..., alias="pageInfo")
    total_count: int = Field(..., alias="totalCount")

    @model_validator(mode="before")
    @classmethod
    def _inflate_from_edges(cls, data):
        if not isinstance(data, dict):
            return data

        if "obtainingTypes" not in data and "obtaining_types" not in data:
            edges = data.get("edges") or []
            data["obtainingTypes"] = [
                (edge or {}).get("node") for edge in edges if (edge or {}).get("node")
            ]

        if "obtaining_types" in data and "obtainingTypes" not in data:
            data["obtainingTypes"] = data["obtaining_types"]

        return data


class GameCategoryInstruction(ApiModel):
    id: str = Field(..., alias="id")
    text: str = Field(..., alias="text")


class GameCategoryInstructionList(ApiModel):
    instructions: List[GameCategoryInstruction] = Field(..., alias="instructions")
    page_info: PageInfo = Field(..., alias="pageInfo")
    total_count: int = Field(..., alias="totalCount")

    @model_validator(mode="before")
    @classmethod
    def _inflate_from_edges(cls, data):
        if not isinstance(data, dict):
            return data

        if "instructions" not in data:
            edges = data.get("edges") or []
            data["instructions"] = [
                (edge or {}).get("node") for edge in edges if (edge or {}).get("node")
            ]
        return data


class GameCategory(ApiModel):
    id: str = Field(..., alias="id")
    slug: str = Field(..., alias="slug")
    name: str = Field(..., alias="name")

    category_id: Optional[str] = Field(None, alias="categoryId")
    game_id: Optional[str] = Field(None, alias="gameId")

    obtaining: Optional[str] = Field(None, alias="obtaining")

    options: Optional[List[GameCategoryOption]] = Field(None, alias="options")
    props: Optional[GameCategoryProps] = Field(None, alias="props")

    no_comment_from_buyer: Optional[bool] = Field(None, alias="noCommentFromBuyer")
    instruction_for_buyer: Optional[str] = Field(None, alias="instructionForBuyer")
    instruction_for_seller: Optional[str] = Field(None, alias="instructionForSeller")

    use_custom_obtaining: Optional[bool] = Field(None, alias="useCustomObtaining")
    auto_confirm_period: Optional[GameCategoryAutoConfirmPeriods] = Field(
        None, alias="autoConfirmPeriod"
    )
    auto_moderation_mode: Optional[bool] = Field(None, alias="autoModerationMode")

    agreements: Optional[List[GameCategoryAgreement]] = Field(None, alias="agreements")
    fee_multiplier: Optional[float] = Field(None, alias="feeMultiplier")


class Game(ApiModel):
    id: str = Field(..., alias="id")
    slug: str = Field(..., alias="slug")
    name: str = Field(..., alias="name")

    type: GameType = Field(..., alias="type")

    logo: File = Field(..., alias="logo")
    banner: Optional[File] = Field(None, alias="banner")

    categories: List[GameCategory] = Field(..., alias="categories")
    created_at: datetime = Field(..., alias="createdAt")


class GameProfile(ApiModel):
    id: str = Field(..., alias="id")
    slug: str = Field(..., alias="slug")
    name: str = Field(..., alias="name")
    type: GameType = Field(..., alias="type")
    logo: File = Field(..., alias="logo")


class GameList(ApiModel):
    games: List[Game] = Field(..., alias="games")
    page_info: PageInfo = Field(..., alias="pageInfo")
    total_count: int = Field(..., alias="totalCount")

    @model_validator(mode="before")
    @classmethod
    def _inflate_from_edges(cls, data):
        if not isinstance(data, dict):
            return data

        if "games" not in data:
            edges = data.get("edges") or []
            data["games"] = [
                (edge or {}).get("node") for edge in edges if (edge or {}).get("node")
            ]
        return data
