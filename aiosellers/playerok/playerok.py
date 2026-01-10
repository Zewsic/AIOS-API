"""High-level Playerok client."""

from __future__ import annotations

from dataclasses import dataclass

from .api import AccountAPI, ChatAPI, DealAPI, GameAPI, ItemAPI
from .client_config import PlayerokClientConfig
from .core.config import PlayerokConfig
from .core.identity_map import IdentityMap
from .entities.chat import Chat
from .entities.deal import Deal
from .entities.game import Game
from .entities.item import Item, MyItem
from .entities.user import User
from .raw import RawAPI
from .transport import PlayerokTransport


@dataclass(slots=True)
class _IdentityMaps:
    """Container for identity maps."""

    users: IdentityMap[str, User]
    chats: IdentityMap[str, Chat]
    deals: IdentityMap[str, Deal]
    games: IdentityMap[str, Game]
    items: IdentityMap[str, Item | MyItem]


class Playerok:
    """
    High-level Playerok client with modular API.

    This class provides a clean, modular interface to the PlayerOK API
    with identity map support and optional client attachment to entities.

    Example:
        >>> config = PlayerokClientConfig(access_token="...")
        >>> async with Playerok(config) as client:
        ...     chat = await client.chats.get("chat_id")
        ...     await chat.send_text("Hello!")
        ...
        ...     deals = await client.deals.list(limit=10)
        ...     for deal in deals:
        ...         await deal.confirm()
    """

    def __init__(self, config: PlayerokClientConfig | str | None = None) -> None:
        """Initialize Playerok client.

        Args:
            config: Client configuration. Can be:
                - PlayerokClientConfig instance
                - str: access token (creates default config)
                - None: creates default config (expects PLAYEROK_ACCESS_TOKEN env var)
        """
        # Support old API: Playerok(access_token="...")
        if isinstance(config, str):
            config = PlayerokClientConfig(access_token=config)
        elif config is None:
            config = PlayerokClientConfig()

        self._config = config
        self._transport: PlayerokTransport | None = None
        self._raw: RawAPI | None = None
        self._use_identity_map = config.use_identity_map
        self._me_id: str | None = None

        # Identity maps for maintaining object identity
        if self._use_identity_map:
            self._identity_maps = _IdentityMaps(
                users=IdentityMap(),
                chats=IdentityMap(),
                deals=IdentityMap(),
                games=IdentityMap(),
                items=IdentityMap(),
            )

        # Modular API
        self.account = AccountAPI(self)
        self.chats = ChatAPI(self)
        self.deals = DealAPI(self)
        self.games = GameAPI(self)
        self.items = ItemAPI(self)

        # Alias for account methods
        self.users = self.account

    async def __aenter__(self) -> Playerok:
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        """Async context manager exit."""
        await self.close()

    async def start(self) -> None:
        """Start the client (initialize transport and fetch account info)."""
        if self._transport is not None:
            return

        # Initialize transport
        self._transport = PlayerokTransport(
            access_token=self._config.access_token,
            config=PlayerokConfig(
                user_agent=self._config.user_agent,
                request_timeout=self._config.request_timeout,
                base_url=self._config.base_url,
            ),
        )
        self._raw = RawAPI(self._transport)

        # Fetch current user ID
        me = await self._raw.account.get_me()
        self._me_id = me.id

    async def close(self) -> None:
        """Close the client and cleanup resources."""
        if self._transport is None:
            return

        await self._transport.close()
        self._transport = None
        self._raw = None

        # Clear identity maps
        if self._use_identity_map:
            self._identity_maps.users.clear()
            self._identity_maps.chats.clear()
            self._identity_maps.deals.clear()
            self._identity_maps.games.clear()
            self._identity_maps.items.clear()
