import os
import random

from .constants import BASE_HEADERS, EXAMPLE_USER_AGENTS


class PlayerokConfig:
    def __init__(
        self,
        *,
        user_agent: str | None = None,
        request_timeout: float | None = None,
        base_url: str | None = None,
    ):
        self.user_agent = user_agent or random.choice(EXAMPLE_USER_AGENTS)
        self.request_timeout = request_timeout or 10.0
        self.base_url = base_url or os.getenv("PLAYEROK_BASE_URL", "https://playerok.com/")

    @property
    def headers(self):
        return BASE_HEADERS | {
            "User-Agent": self.user_agent,
        }
