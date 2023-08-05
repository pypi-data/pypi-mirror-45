from . import handler_request
from .routes import charge_routes


def cancel(id, dictionary={}):
    return handler_request.post(charge_routes.CANCEL_CHARGE_LINK.format(id), dictionary)


def create(dictionary):
    return handler_request.post(charge_routes.CHARGE_LINK, dictionary)


def find(id):
    return handler_request.get(charge_routes.CHARGE_LINK_GET.format(id))


def find_all():
    return handler_request.get(charge_routes.CHARGE_LINK)


def billet(id):
    return handler_request.get(charge_routes.BILLET_LINK.format(id))


def cancel_billet(id, dictionary={}):
    return handler_request.post(charge_routes.CANCEL_BILLET_LINK.format(id), dictionary)
