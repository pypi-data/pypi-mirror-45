from rakuten_pay import checkout
from rakuten_pay import handler_request


class TestCategory:

    def test_category_find_all(self):
        handler_request.authentication_key('77753821000123', 'EBDB6843FAA9073B5AD1929A77CBF86B')
        resp = checkout.get('81783912000189', 100.00)
        assert resp['result'] == 'success'