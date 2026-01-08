from enum import StrEnum


class QueryID(StrEnum):
    user = "2e2e3b656d2ba48e0b2cd5eeedf88ef70e4aabb4ac4d9d9e9b8feff343a37d98"
    deals = "c3b623b5fe0758cf91b2335ebf36ff65f8650a6672a792a3ca7a36d270d396fb"
    deal = "5652037a966d8da6d41180b0be8226051fe0ed1357d460c6ae348c3138a0fba3"
    games = "5de9b3240c148579c82e2310a30b4aad5462884fd1abf93dd3c43d1f5ef14d85"
    game = "4775f8630a3e234c50537e68649043ac32a40b0370b0f1fb2dc314500ef6202d"
    game_category = "d81943c23bc558591f70286ad69bb6bf7f6229d04aae39fb0a9701d78a9fd749"
    game_category_agreements = "3ea4b047196ed9f84aa5eb652299c4bd73f2e99e9fdf4587877658d9ea6330f6"
    game_category_obtaining_types = (
        "15b0991414821528251930b4c8161c299eb39882fd635dd5adb1a81fb0570aea"
    )
    game_category_instructions = "5991cead6a8ca46195bc4f7ae3164e7606105dbb82834c910658edeb0a1d1918"
    game_category_data_fields = "6fdadfb9b05880ce2d307a1412bc4f2e383683061c281e2b65a93f7266ea4a49"
    chats = "999f86b7c94a4cb525ed5549d8f24d0d24036214f02a213e8fd7cefc742bbd58"
    chat = "bb024dc0652fc7c1302a64a117d56d99fb0d726eb4b896ca803dca55f611d933"
    chat_messages = "e8162a8500865f4bb18dbaacb1c4703823f74c1925a91a5103f41c2021f0557a"
    items = "206ae9d63e58bc41df9023aae39b9136f358282a808c32ee95f5b8b6669a8c8b"
    item = "5b2be2b532cea7023f4f584512c4677469858e2210349f7eec78e3b96d563716"
    item_priority_statuses = "b922220c6f979537e1b99de6af8f5c13727daeff66727f679f07f986ce1c025a"
    transaction_providers = "31960e5dd929834c1f85bc685db80657ff576373076f016b2578c0a34e6e9f42"
    transactions = "3b9925106c3fe9308ac632254fd70da347b5701f243ab8690477d5a7ca37c2c8"
    sbp_bank_members = "ef7902598e855fa15fb5e3112156ac226180f0b009a36606fc80a18f00b80c63"
    verified_cards = "eb338d8432981307a2b3d322b3310b2447cab3a6acf21aba4b8773b97e72d1aa"


class GameType(StrEnum):
    GAME = "GAME"
    APPLICATION = "APPLICATION"


class UserType(StrEnum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    BOT = "BOT"


class GameCategoryDataFieldTypes(StrEnum):
    ITEM_DATA = "ITEM_DATA"
    OBTAINING_DATA = "OBTAINING_DATA"


class EventTypes(StrEnum):
    CHAT_INITIALIZED = "CHAT_INITIALIZED"
    NEW_MESSAGE = "NEW_MESSAGE"
    NEW_DEAL = "NEW_DEAL"
    NEW_REVIEW = "NEW_REVIEW"
    DEAL_CONFIRMED = "DEAL_CONFIRMED"
    DEAL_CONFIRMED_AUTOMATICALLY = "DEAL_CONFIRMED_AUTOMATICALLY"
    DEAL_ROLLED_BACK = "DEAL_ROLLED_BACK"
    DEAL_HAS_PROBLEM = "DEAL_HAS_PROBLEM"
    DEAL_PROBLEM_RESOLVED = "DEAL_PROBLEM_RESOLVED"
    DEAL_STATUS_CHANGED = "DEAL_STATUS_CHANGED"
    ITEM_PAID = "ITEM_PAID"
    ITEM_SENT = "ITEM_SENT"


class ItemLogEvents(StrEnum):
    PAID = "PAID"
    SENT = "SENT"
    DEAL_CONFIRMED = "DEAL_CONFIRMED"
    DEAL_ROLLED_BACK = "DEAL_ROLLED_BACK"
    PROBLEM_REPORTED = "PROBLEM_REPORTED"
    PROBLEM_RESOLVED = "PROBLEM_RESOLVED"


class TransactionOperations(StrEnum):
    DEPOSIT = "DEPOSIT"
    BUY = "BUY"
    SELL = "SELL"
    ITEM_DEFAULT_PRIORITY = "ITEM_DEFAULT_PRIORITY"
    ITEM_PREMIUM_PRIORITY = "ITEM_PREMIUM_PRIORITY"
    WITHDRAW = "WITHDRAW"
    MANUAL_BALANCE_INCREASE = "MANUAL_BALANCE_INCREASE"
    MANUAL_BALANCE_DECREASE = "MANUAL_BALANCE_DECREASE"
    REFERRAL_BONUS = "REFERRAL_BONUS"
    STEAM_DEPOSIT = "STEAM_DEPOSIT"


class TransactionDirections(StrEnum):
    IN = "IN"
    OUT = "OUT"


class TransactionStatuses(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    CONFIRMED = "CONFIRMED"
    ROLLED_BACK = "ROLLED_BACK"
    FAILED = "FAILED"


class TransactionPaymentMethodIds(StrEnum):
    MIR = "MIR"
    VISA_MASTERCARD = "VISA_MASTERCARD"
    ERIP = "ERIP"


class TransactionProviderDirections(StrEnum):
    IN = "IN"
    OUT = "OUT"


class TransactionProviderIds(StrEnum):
    LOCAL = "LOCAL"
    SBP = "SBP"
    BANK_CARD_RU = "BANK_CARD_RU"
    BANK_CARD_BY = "BANK_CARD_BY"
    BANK_CARD = "BANK_CARD"
    YMONEY = "YMONEY"
    USDT = "USDT"
    PENDING_INCOME = "PENDING_INCOME"


class BankCardTypes(StrEnum):
    MIR = "MIR"
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"


class ItemDealStatuses(StrEnum):
    PAID = "PAID"
    PENDING = "PENDING"
    SENT = "SENT"
    CONFIRMED = "CONFIRMED"
    ROLLED_BACK = "ROLLED_BACK"


class ItemDealDirections(StrEnum):
    IN = "IN"
    OUT = "OUT"


class ChatTypes(StrEnum):
    PM = "PM"
    NOTIFICATIONS = "NOTIFICATIONS"
    SUPPORT = "SUPPORT"


class ChatStatuses(StrEnum):
    NEW = "NEW"
    FINISHED = "FINISHED"


class ChatMessageButtonTypes(StrEnum):
    # TODO: Add another types of buttons
    REDIRECT = "REDIRECT"
    LOTTERY = "LOTTERY"
    ASK_FOR_EXTERNAL_REVIEW = "ASK_FOR_EXTERNAL_REVIEW"


class ItemStatuses(StrEnum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    PENDING_MODERATION = "PENDING_MODERATION"
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"
    BLOCKED = "BLOCKED"
    EXPIRED = "EXPIRED"
    SOLD = "SOLD"
    DRAFT = "DRAFT"


class ReviewStatuses(StrEnum):
    APPROVED = "APPROVED"
    DELETED = "DELETED"


class SortDirections(StrEnum):
    DESC = "DESC"
    ASC = "ASC"


class ItemsSortOptions(StrEnum):
    PRICE_ASC = "PRICE_ASC"
    PRICE_DESC = "PRICE_DESC"
    RATING_ASC = "RATING_ASC"
    RATING_DESC = "RATING_DESC"
    DEFAULT = "DEFAULT"


class PriorityTypes(StrEnum):
    DEFAULT = "DEFAULT"
    PREMIUM = "PREMIUM"


class GameCategoryAgreementIconTypes(StrEnum):
    # TODO: Add another types of icons
    RESTRICTION = "RESTRICTION"
    CONFIRMATION = "CONFIRMATION"


class GameCategoryOptionTypes(StrEnum):
    # TODO: Add another types of options
    SELECTOR = "SELECTOR"
    SWITCH = "SWITCH"


class GameCategoryDataFieldInputTypes(StrEnum):
    # Maybe, another obtaining types can be exists
    INPUT = "INPUT"
    TEXTAREA = "TEXTAREA"


class GameCategoryAutoConfirmPeriods(StrEnum):
    # TODO: Add all confirm periods
    SEVEN_DAYS = "SEVEN_DAYS"


class GameCategoryInstructionTypes(StrEnum):
    FOR_SELLER = "FOR_SELLER"
    FOR_BUYER = "FOR_BUYER"
