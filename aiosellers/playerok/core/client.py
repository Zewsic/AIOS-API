import os
from typing import Any, Literal

from tls_requests import AsyncClient, Response

from .config import PlayerokConfig
from .constants import CLOUDFLARE_SIGNATURES
from .exceptions import CloudflareDetected


class PlayerokClient:
    def __init__(self, access_token: str | None = None, config: PlayerokConfig | None = None):
        self._access_token = access_token or os.getenv("PLAYEROK_ACCESS_TOKEN")
        self._config = config or PlayerokConfig()

        if not self._access_token:
            raise RuntimeError(
                "Please provide playerok access token or fill PLAYEROK_ACCESS_TOKEN environment variable."
            )

        # Initialize network client
        self._client = AsyncClient(
            cookies={"token": self._access_token},
            headers=self._config.headers,
            timeout=self._config.request_timeout,
        )

    @staticmethod
    def _raise_if_cloudflare(response: Response):
        if any(sig in response.text for sig in CLOUDFLARE_SIGNATURES):
            raise CloudflareDetected("The cloudflare protection is detected.")

    async def request(
        self,
        method: Literal["get", "post"],
        url: str,
        payload: dict[str, str],
        *,
        headers: dict[str, str] | None = None,
        files: dict[str, Any] | None = None,
    ) -> Response:
        request_headers = self._config.headers.copy()
        if headers is not None:
            request_headers.update(headers)
        if not url.startswith("http"):
            url = self._config.base_url + url

        if method == "get":
            response = await self._client.get(url=url, headers=request_headers, params=payload)
        elif method == "post":
            if files:
                response = await self._client.post(
                    url=url, headers=request_headers, data=payload, files=files
                )
            else:
                response = await self._client.post(url=url, headers=request_headers, json=payload)
        else:
            raise RuntimeError(f"Unsupported HTTP method: {method}")

        self._raise_if_cloudflare(response)
        return response

    async def close(self):
        await self._client.aclose()
