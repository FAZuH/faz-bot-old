class HunterBotError(Exception):
    """Base error class for all library-related exceptions in this file.
    Essentially, this could be caught to handle any exceptions thrown from this library.
    """

class HTTPError(HunterBotError):
    """Base error class for all HTTP-related exceptions in this file."""


class BadRequest(HTTPError):
    """HTTP 400. The server could not process our request, likely due to an error of ours."""


class Unauthorized(HTTPError):
    """HTTP 401. We are not authorized to access the requested resource.
    This can occur due to an invalid or expired Bearer token.
    """


class Forbidden(HTTPError):
    """HTTP 403. We do not have permission to access the requested resource."""


class NotFound(HTTPError):
    """HTTP 404. This resource does not exist."""


class ServerError(HTTPError):
    """HTTP 5xx. The server encountered an unexpected condition that prevented it from fulfilling the request."""


class TooManyRetries(HTTPError):
    """Exceeded maximum number of retries."""


class Ratelimited(HTTPError):
    """HTTP 429. The server is ratelimiting us. Please wait for a bit before trying again."""
