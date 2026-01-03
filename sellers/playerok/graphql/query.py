import json

from ..models import QueryID


class GraphQLQuery:
    @staticmethod
    def get_me():
        return {
            "operationName": "viewer",
            "variables": {},
            "query": "query viewer {\n  viewer {\n    ...Viewer\n    __typename\n  }\n}\n\nfragment Viewer on User {\n  id\n  username\n  email\n  role\n  hasFrozenBalance\n  supportChatId\n  systemChatId\n  unreadChatsCounter\n  isBlocked\n  isBlockedFor\n  isFundsProtectionActive\n  createdAt\n  lastItemCreatedAt\n  hasConfirmedPhoneNumber\n  canPublishItems\n  chosenVerifiedCard {\n    ...MinimalUserBankCard\n    __typename\n  }\n  profile {\n    id\n    avatarURL\n    testimonialCounter\n    __typename\n  }\n  __typename\n}\n\nfragment MinimalUserBankCard on UserBankCard {\n  id\n  cardFirstSix\n  cardLastFour\n  cardType\n  isChosen\n  __typename\n}",
        }

    @staticmethod
    def get_user(username: str | None = None, id: str | None = None):
        return {
            "operationName": "user",
            "variables": {"id": id, "username": username, "hasSupportAccess": False},
            "extensions": {"persistedQuery": {"version": 1, "sha256Hash": QueryID.user.value}}
        }
