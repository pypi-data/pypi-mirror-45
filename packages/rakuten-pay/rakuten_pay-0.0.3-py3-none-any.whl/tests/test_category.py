from rakuten_pay import category
from rakuten_pay import handler_request


class TestCategory:

    def test_category_find_all(self):
        handler_request.authentication_key('77753821000123', 'EBDB6843FAA9073B5AD1929A77CBF86B')
        resp = category.find_all()
        assert resp['result'] == 'success'