from datetime import datetime
from typing import Any

from pydantic import AliasChoices, Field

from . import ApiModel, UserType


class Account(ApiModel):
    id: str = Field(..., alias="id")
    username: str = Field(..., alias="username")
    email: str = Field(..., alias="email")
    role: UserType = Field(..., alias="role")
    has_frozen_balance: bool = Field(..., alias="hasFrozenBalance")
    support_chat_id: str = Field(..., alias="supportChatId")
    system_chat_id: str = Field(..., alias="systemChatId")
    unread_chats_counter: int = Field(..., alias="unreadChatsCounter")
    is_blocked: bool = Field(..., alias="isBlocked")
    is_blocked_for: Any = Field(None, alias="isBlockedFor")
    created_at: datetime = Field(..., alias="createdAt")
    last_item_created_at: datetime = Field(None, alias="lastItemCreatedAt")
    has_confirmed_phone_number: bool = Field(..., alias="hasConfirmedPhoneNumber")
    can_publish_items: bool = Field(..., alias="canPublishItems")
    is_funds_protection_active: bool = Field(..., alias="isFundsProtectionActive")
    chosen_verified_card: Any = Field(None, alias="chosenVerifiedCard")


class UserProfile(ApiModel):
    id: str = Field(..., alias="id")
    username: str = Field(..., alias="username")
    role: UserType = Field(UserType.USER, alias="role")
    avatar_url: str | None = Field(None, alias="avatarURL")
    is_online: bool | None = Field(None, alias="isOnline")
    is_blocked: bool = Field(False, alias="isBlocked")
    rating: float | None = Field(None, alias="rating")
    reviews_count: int | None = Field(
        None,
        alias="reviewsCount",
        validation_alias=AliasChoices("reviewsCount", "testimonialCounter"),
    )
    created_at: datetime | None = Field(None, alias="createdAt")


class AccountBalance(ApiModel):
    id: str = Field(..., alias="id")
    value: float = Field(..., alias="value")  # Total balance
    available: float = Field(..., alias="available")  # Unlocked balance for purchasing items
    frozen: float = Field(..., alias="frozen")  # idk
    pending_income: float = Field(
        ..., alias="pendingIncome"
    )  # Unlockable balance (after up to 48 hours). Can be wasted for premium
    withdrawable: float = Field(
        ..., alias="withdrawable"
    )  # Balance that can be withdrawn right now.


class AccountItemsStats(ApiModel):
    total: int = Field(..., alias="total")
    finished: int = Field(..., alias="finished")


class AccountIncomingDealsStats(ApiModel):
    total: int = Field(..., alias="total")
    finished: int = Field(..., alias="finished")


class AccountOutgoingDealsStats(ApiModel):
    total: int = Field(..., alias="total")
    finished: int = Field(..., alias="finished")


class AccountDealsStats(ApiModel):
    incoming: AccountIncomingDealsStats = Field(..., alias="incoming")
    outgoing: AccountOutgoingDealsStats = Field(..., alias="outgoing")


class AccountStats(ApiModel):
    items: AccountItemsStats = Field(..., alias="items")
    deals: AccountDealsStats = Field(..., alias="deals")


class AccountProfile(UserProfile):
    email: str = Field(..., alias="email")
    balance: AccountBalance = Field(..., alias="balance")
    stats: AccountStats = Field(..., alias="stats")
    is_blocked_for: Any = Field(None, alias="isBlockedFor")
    is_verified: bool | None = Field(None, alias="isVerified")
    has_frozen_balance: bool = Field(..., alias="hasFrozenBalance")
    has_enabled_notifications: bool = Field(..., alias="hasEnabledNotifications")
    support_chat_id: str = Field(..., alias="supportChatId")
    system_chat_id: str = Field(..., alias="systemChatId")
