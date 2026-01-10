"""Client configuration for Playerok."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlayerokClientConfig:
    """Configuration for Playerok client.

    Attributes:
        access_token: PlayerOK access token (or set PLAYEROK_ACCESS_TOKEN env var)
        user_agent: Custom user agent string
        request_timeout: Request timeout in seconds
        base_url: Base URL for PlayerOK API
        use_identity_map: Enable identity map for maintaining object identity
    """

    access_token: str | None = None
    user_agent: str | None = None
    request_timeout: float = 10.0
    base_url: str = "https://playerok.com/"
    use_identity_map: bool = True
