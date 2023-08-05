from rakuten_pay_pkg.routes.base_routes import BASE_URL

CHARGE_LINK = BASE_URL + '/rpay/v1/charges'

CHARGE_LINK_GET = CHARGE_LINK + '/{0}'

CANCEL_CHARGE_LINK = CHARGE_LINK + '/{0}/refund'

BILLET_LINK = CHARGE_LINK + '/{0}/billet'

CANCEL_BILLET_LINK = CHARGE_LINK + '/{0}/cancel'
