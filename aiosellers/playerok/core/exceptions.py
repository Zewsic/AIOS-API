class CloudflareDetected(Exception):
    pass


class Unauthorized(Exception):
    pass


class GraphQLError(Exception):
    pass


class UnsupportedPaymentProvider(Exception):
    pass
