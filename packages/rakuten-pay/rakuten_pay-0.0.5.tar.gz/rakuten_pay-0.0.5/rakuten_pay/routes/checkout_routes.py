from rakuten_pay.routes.base_routes import BASE_URL

CHECKOUT_LINK = BASE_URL + '/rpay/v1/checkout'

CHECKOUT_DATA_LINK = CHECKOUT_LINK + '?customer_document={0}&amount={1}'
