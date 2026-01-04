from datetime import datetime
from typing import Any

from pydantic import Field, model_validator

from . import (
    ApiModel,
    BankCardTypes,
    PageInfo,
    TransactionDirections,
    TransactionOperations,
    TransactionPaymentMethodIds,
    TransactionProviderIds,
    TransactionStatuses,
)
from .account import UserProfile


class SBPBankMember(ApiModel):
    id: str = Field(..., alias="id")
    name: str = Field(..., alias="name")
    icon: str | None = Field(None, alias="icon")


class TransactionProviderLimitRange(ApiModel):
    min: float = Field(..., alias="min")
    max: float = Field(..., alias="max")


class TransactionProviderLimits(ApiModel):
    incoming: TransactionProviderLimitRange = Field(..., alias="incoming")
    outgoing: TransactionProviderLimitRange = Field(..., alias="outgoing")


class TransactionProviderRequiredUserData(ApiModel):
    email: bool = Field(..., alias="email")
    phone_number: bool = Field(..., alias="phoneNumber")
    erip_account_number: bool | None = Field(None, alias="eripAccountNumber")


class TransactionProviderProps(ApiModel):
    required_user_data: TransactionProviderRequiredUserData = Field(..., alias="requiredUserData")
    tooltip: str | None = Field(None, alias="tooltip")


class TransactionPaymentMethod(ApiModel):
    id: TransactionPaymentMethodIds = Field(..., alias="id")
    name: str = Field(..., alias="name")
    fee: float = Field(..., alias="fee")
    provider_id: TransactionProviderIds = Field(..., alias="providerId")
    account: Any | None = Field(None, alias="account")  # AccountProfile
    props: TransactionProviderProps = Field(..., alias="props")
    limits: TransactionProviderLimits = Field(..., alias="limits")


class TransactionProvider(ApiModel):
    id: TransactionProviderIds = Field(..., alias="id")
    name: str = Field(..., alias="name")
    fee: float = Field(..., alias="fee")
    min_fee_amount: float | None = Field(None, alias="minFeeAmount")
    description: str | None = Field(None, alias="description")
    account: Any | None = Field(None, alias="account")  # AccountProfile
    props: TransactionProviderProps = Field(..., alias="props")
    limits: TransactionProviderLimits = Field(..., alias="limits")
    payment_methods: list[TransactionPaymentMethod] | None = Field(None, alias="paymentMethods")


class Transaction(ApiModel):
    id: str = Field(..., alias="id")
    operation: TransactionOperations | None = Field(None, alias="operation")
    direction: TransactionDirections | None = Field(None, alias="direction")
    provider_id: TransactionProviderIds | None = Field(None, alias="providerId")
    provider: TransactionProvider | None = Field(None, alias="provider")
    user: UserProfile | None = Field(None, alias="user")
    creator: UserProfile | None = Field(None, alias="creator")
    status: TransactionStatuses | None = Field(None, alias="status")
    status_description: str | None = Field(None, alias="statusDescription")
    status_expiration_date: datetime | None = Field(None, alias="statusExpirationDate")
    value: float | None = Field(None, alias="value")
    fee: float | None = Field(None, alias="fee")
    created_at: datetime | None = Field(None, alias="createdAt")
    verified_at: datetime | None = Field(None, alias="verifiedAt")
    verified_by: UserProfile | None = Field(None, alias="verifiedBy")
    completed_at: datetime | None = Field(None, alias="completedAt")
    completed_by: UserProfile | None = Field(None, alias="completedBy")
    payment_method_id: str | None = Field(None, alias="paymentMethodId")
    is_suspicious: bool | None = Field(None, alias="isSuspicious")
    sbp_bank_name: str | None = Field(None, alias="spbBankName")


class TransactionList(ApiModel):
    transactions: list[Transaction] = Field(..., alias="transactions")
    page_info: PageInfo = Field(..., alias="pageInfo")
    total_count: int = Field(..., alias="totalCount")

    @model_validator(mode="before")
    @classmethod
    def _inflate_from_edges(cls, data):
        if not isinstance(data, dict):
            return data

        if "transactions" not in data:
            edges = data.get("edges") or []
            data["transactions"] = [
                (edge or {}).get("node") for edge in edges if (edge or {}).get("node")
            ]
        return data


class UserBankCard(ApiModel):
    id: str = Field(..., alias="id")
    card_first_six: str = Field(..., alias="cardFirstSix")
    card_last_four: str = Field(..., alias="cardLastFour")
    card_type: BankCardTypes = Field(..., alias="cardType")
    is_chosen: bool = Field(..., alias="isChosen")


class UserBankCardList(ApiModel):
    bank_cards: list[UserBankCard] = Field(..., alias="bankCards")
    page_info: PageInfo = Field(..., alias="pageInfo")
    total_count: int = Field(..., alias="totalCount")

    @model_validator(mode="before")
    @classmethod
    def _inflate_from_edges(cls, data):
        if not isinstance(data, dict):
            return data

        if "bankCards" not in data:
            edges = data.get("edges") or []
            data["bankCards"] = [
                (edge or {}).get("node") for edge in edges if (edge or {}).get("node")
            ]
        return data
