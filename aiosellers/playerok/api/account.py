"""Account API module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..entities.user import User
from ..schemas import Account, AccountProfile

if TYPE_CHECKING:
    from ..playerok import Playerok


class AccountAPI:
    """Account-related API methods."""

    def __init__(self, client: Playerok) -> None:
        self._client = client

    async def me(self) -> Account:
        """Get current account info.

        Returns:
            Account object with basic account information.

        Raises:
            Unauthorized: If access token is invalid.
        """
        return await self._client._raw.account.get_me()

    async def profile(self) -> AccountProfile:
        """Get current account profile with balance and other details.

        Returns:
            AccountProfile object with full profile information.
        """
        me = await self.me()
        return await self._client._raw.account.get_account(me.username)

    async def get_user(
        self,
        user_id: str | None = None,
        *,
        username: str | None = None,
        force_refresh: bool = False,
    ) -> User:
        """Get user by ID or username.

        Args:
            user_id: User ID to fetch.
            username: Username to fetch.
            force_refresh: If True, bypass identity map and fetch fresh data.

        Returns:
            User entity with client attached.
        """
        if user_id is None and username is None:
            raise ValueError("Either user_id or username must be provided")

        # Check identity map first (only by ID)
        if user_id and not force_refresh and self._client._use_identity_map:
            cached = self._client._identity_maps.users.get(user_id)
            if cached:
                return cached

        # Fetch from API
        profile = await self._client._raw.account.get_user(id=user_id, username=username)
        if profile is None:
            if user_id:
                # Create stub user with just ID
                user = User(id=user_id)
            else:
                raise ValueError(f"User with username '{username}' not found")
        else:
            user = User(
                id=profile.id,
                username=profile.username,
                avatar_url=profile.avatar_url,
                role=profile.role,
                is_online=profile.is_online,
                is_blocked=profile.is_blocked,
                rating=profile.rating,
                reviews_count=profile.reviews_count,
            )

        # Attach client
        user._client = self._client

        # Store in identity map
        if self._client._use_identity_map:
            self._client._identity_maps.users.set(user.id, user)

        return user
