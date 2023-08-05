from rakuten_pay_pkg import charge

from resources import handler_request


class TestCharge:

    def test_charge_find_all(self):
        handler_request.authentication_key('77753821000123', 'EBDB6843FAA9073B5AD1929A77CBF86B')
        resp = charge.find_all()
        assert resp['result'] == 'success'

    def test_charge_create_credit_card(self):
        handler_request.authentication_key('77753821000123', 'EBDB6843FAA9073B5AD1929A77CBF86B')

        dict = {
            "webhook_url": "http://localhost/loja/minha-conta",
            "reference": "Pedido#001",
            "payments": [
                {
                    "token": "180629201112Q7pzBWdogZFXm8tM5771",
                    "reference": "1",
                    "options": {
                        "save_card": False,
                        "recurrency": False,
                        "new_card": False
                    },
                    "method": "credit_card",
                    "installments_quantity": 1,
                    "holder_name": "CLIENTE DE TESTE",
                    "holder_document": "12345678909",
                    "expires_on": "2026-01-01",
                    "cvv": "123",
                    "brand": "mastercard",
                    "amount": 100.00
                }
            ],
            "order": {
                "taxes_amount": 0,
                "shipping_amount": 0,
                "reference": "001",
                "payer_ip": "::1",
                "items_amount": 100.0,
                "items": [
                    {
                        "total_amount": 100.00,
                        "reference": "001",
                        "quantity": 1,
                        "description": "PRODUTO TESTE",
                        "categories": [
                            {
                                "name": "Outros",
                                "id": "001"
                            }
                        ],
                        "amount": 100.00
                    }
                ],
                "discount_amount": 0
            },
            "fingerprint": "5ed7ae9e8817818f6ed17b6f4ee83350-9gna953vpwajz0e4m92",
            "customer": {
                "phones": [
                    {
                        "reference": "mobile",
                        "number": {
                            "number": "999999999",
                            "country_code": "55",
                            "area_code": "11"
                        },
                        "kind": "billing"
                    },
                    {
                        "reference": "mobile",
                        "number": {
                            "number": "999999999",
                            "country_code": "55",
                            "area_code": "11"
                        },
                        "kind": "shipping"
                    }
                ],
                "name": "CLIENTE DE TESTE",
                "kind": "personal",
                "email": "cliente@example.com",
                "document": "12345678909",
                "business_name": "CLIENTE DE TESTE",
                "birth_date": "1970-01-01",
                "addresses": [
                    {
                        "zipcode": "05001-100",
                        "street": "Av. Francisco Matarazzo",
                        "state": "SP",
                        "number": "1500",
                        "kind": "billing",
                        "district": "Barra Funda",
                        "country": "BR",
                        "contact": "CLIENTE DE TESTE",
                        "complement": "Conj. New York, 6º Andar",
                        "city": "São Paulo"
                    },
                    {
                        "zipcode": "05001-100",
                        "street": "Av. Francisco Matarazzo",
                        "state": "SP",
                        "number": "1500",
                        "kind": "shipping",
                        "district": "Barra Funda",
                        "country": "BR",
                        "contact": "CLIENTE DE TESTE",
                        "complement": "Conj. New York, 6º Andar",
                        "city": "São Paulo"
                    }
                ]
            },
            "currency": "BRL",
            "amount": 100.00
        }

        resp = charge.create(dict)
        assert resp['result'] == 'success'

    def test_charge_create_billet(self):
        handler_request.authentication_key('77753821000123', 'EBDB6843FAA9073B5AD1929A77CBF86B')

        dict = {
            "webhook_url": "http://localhost/loja/minha-conta",
            "reference": "Pedido#006",
            "payments": [
                {
                    "reference": "Pedido#006",
                    "method": "billet",
                    "amount": 100.00
                }
            ],
            "order": {
                "taxes_amount": 0,
                "shipping_amount": 0,
                "reference": "001",
                "payer_ip": "::1",
                "items_amount": 100.0,
                "items": [
                    {
                        "total_amount": 100.00,
                        "reference": "001",
                        "quantity": 1,
                        "description": "PRODUTO TESTE",
                        "amount": 100.00
                    }
                ],
                "discount_amount": 0
            },
            "fingerprint": "5ed7ae9e8817818f6ed17b6f4ee83350-9gna953vpwajz0e4m92",
            "customer": {
                "phones": [
                    {
                        "reference": "mobile",
                        "number": {
                            "number": "999999999",
                            "country_code": "55",
                            "area_code": "11"
                        },
                        "kind": "billing"
                    },
                    {
                        "reference": "mobile",
                        "number": {
                            "number": "999999999",
                            "country_code": "55",
                            "area_code": "11"
                        },
                        "kind": "shipping"
                    }
                ],
                "name": "CLIENTE DE TESTE",
                "kind": "personal",
                "email": "cliente@example.com",
                "document": "12345678909",
                "business_name": "CLIENTE DE TESTE",
                "birth_date": "1970-01-01",
                "addresses": [
                    {
                        "zipcode": "05001-100",
                        "street": "Av. Francisco Matarazzo",
                        "state": "SP",
                        "number": "1500",
                        "kind": "billing",
                        "district": "Barra Funda",
                        "country": "BR",
                        "contact": "CLIENTE DE TESTE",
                        "complement": "Conj. New York, 6º Andar",
                        "city": "São Paulo"
                    },
                    {
                        "zipcode": "05001-100",
                        "street": "Av. Francisco Matarazzo",
                        "state": "SP",
                        "number": "1500",
                        "kind": "shipping",
                        "district": "Barra Funda",
                        "country": "BR",
                        "contact": "CLIENTE DE TESTE",
                        "complement": "Conj. New York, 6º Andar",
                        "city": "São Paulo"
                    }
                ]
            },
            "currency": "BRL",
            "amount": 100.00
        }

        resp = charge.create(dict)
        assert resp['result'] == 'success'