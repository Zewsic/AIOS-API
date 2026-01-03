from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, AliasChoices


class Account(BaseModel):
    id: str = Field(..., alias="id")
    username: str = Field(..., alias="username")
    email: str = Field(..., alias="email")
    role: str = Field(..., alias="role")
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


class UserProfile(BaseModel):
    id: str = Field(..., alias="id")
    username: str = Field(..., alias="username")
    role: str = Field(..., alias="role")
    avatar_url: Optional[str] = Field(None, alias="avatarURL")
    is_online: Optional[bool] = Field(None, alias="isOnline")
    is_blocked: bool = Field(..., alias="isBlocked")
    rating: Optional[float] = Field(None, alias="rating")
    reviews_count: Optional[int] = Field(None, alias="reviewsCount", validation_alias=AliasChoices("reviewsCount", "testimonialCounter"))
    created_at: Optional[datetime] = Field(None, alias="createdAt")


class AccountBalance(BaseModel):
    id: str = Field(..., alias="id")
    value: float = Field(..., alias="value")
    available: float = Field(..., alias="available")
    frozen: float = Field(..., alias="frozen")
    pending_income: float = Field(..., alias="pendingIncome")
    withdrawable: float = Field(..., alias="withdrawable")


class AccountItemsStats(BaseModel):
    total: int = Field(..., alias="total")
    finished: int = Field(..., alias="finished")


class AccountIncomingDealsStats(BaseModel):
    total: int = Field(..., alias="total")
    finished: int = Field(..., alias="finished")


class AccountOutgoingDealsStats(BaseModel):
    total: int = Field(..., alias="total")
    finished: int = Field(..., alias="finished")


class AccountDealsStats(BaseModel):
    incoming: AccountIncomingDealsStats = Field(..., alias="incoming")
    outgoing: AccountOutgoingDealsStats = Field(..., alias="outgoing")


class AccountStats(BaseModel):
    items: AccountItemsStats = Field(..., alias="items")
    deals: AccountDealsStats = Field(..., alias="deals")


class AccountProfile(UserProfile):
    email: str = Field(..., alias="email")
    balance: AccountBalance = Field(..., alias="balance")
    stats: AccountStats = Field(..., alias="stats")
    is_blocked_for: Any = Field(None, alias="isBlockedFor")
    is_verified: Optional[bool] = Field(None, alias="isVerified")
    has_frozen_balance: bool = Field(..., alias="hasFrozenBalance")
    has_enabled_notifications: bool = Field(..., alias="hasEnabledNotifications")
    support_chat_id: str = Field(..., alias="supportChatId")
    system_chat_id: str = Field(..., alias="systemChatId")
