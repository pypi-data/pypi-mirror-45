from . import handler_request
from .routes import checkout_routes


def get(document, value):
    return handler_request.get(checkout_routes.CHECKOUT_DATA_LINK.format(document, value))
