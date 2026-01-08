from ..transport import PlayerokTransport
from .account import RawAccountService
from .chats import RawChatService
from .deals import RawDealsService
from .games import RawGamesService
from .items import RawItemsService
from .transactions import RawTransactionService


class RawAPI:
    """
    Low-level API access (raw GraphQL + parsing into Schema models).

    This layer has:
    - no caching
    - no domain methods
    - no cross-service orchestration
    """

    def __init__(self, transport: PlayerokTransport):
        self.account = RawAccountService(transport)
        self.chats = RawChatService(transport)
        self.deals = RawDealsService(transport)
        self.games = RawGamesService(transport)
        self.items = RawItemsService(transport)
        self.transactions = RawTransactionService(transport)


__all__ = [
    "RawAPI",
    "RawAccountService",
    "RawChatService",
    "RawDealsService",
    "RawGamesService",
    "RawItemsService",
    "RawTransactionService",
]
