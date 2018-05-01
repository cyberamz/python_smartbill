import datetime
from unittest import TestCase

from .config import SMARTBILL_TOKEN, SMARTBILL_USER, SMARTBILL_CIF
from smartbill import SmartBill

class SmartBillTest(TestCase):

    def setUp(self):
        self.smartbill = SmartBill(SMARTBILL_USER, SMARTBILL_TOKEN, SMARTBILL_CIF)

    def test_authenticate(self):
        self.assertTrue('authorization' in self.smartbill.headers)

    def test_get_tax(self):
        self.assertDictEqual(self.smartbill.get_tax(), {'errorText': '',
                                                    'message': '',
                                                    'number': '',
                                                    'series': '',
                                                    'url': '',
                                                    'taxes': [{'name': 'Normala', 'percentage': 19.0},
                                                              {'name': 'Redusa', 'percentage': 9.0},
                                                              {'name': 'SFDD', 'percentage': 0.0},
                                                              {'name': 'SDD', 'percentage': 0.0},
                                                              {'name': 'TVA Inclus', 'percentage': 0.0},
                                                              {'name': 'Taxare inversa', 'percentage': 0.0},
                                                              {'name': 'Redusa', 'percentage': 5.0},
                                                              {'name': 'Veche', 'percentage': 24.0},
                                                              {'name': 'Veche', 'percentage': 20.0}]
                                                    })

    def test_get_series(self):
        self.assertEqual(self.smartbill.get_series()['list'][0]['name'], 'C')

    def test_create_invoice_service(self):
        product = self.smartbill.create_product(name_product='Service name', code='test',
                                                measuring_unit_name='h', quantify=10, price=10,
                                                is_tax_included=True, tax_name='Redusa', tax_percentage=9,
                                                is_service=True)
        client = self.smartbill.create_client(name_client='test', country_client="Romania")
        invoice = self.smartbill.create_invoice(client, [product], issue_date="2018-02-02")
        self.assertEqual(invoice['series'], 'C')

    def test_create_invoice_product(self):
        product = self.smartbill.create_product(name_product='Caps21or', code='MK002',
                                                measuring_unit_name='buc', quantify=1, price=10,
                                                is_tax_included=True, tax_name='Redusa', tax_percentage=9,
                                                is_service=False, use_stock=True, ware_house_name='Amazon2')
        product2 = self.smartbill.create_product(name_product='Service name', code='test',
                                                measuring_unit_name='h', quantify=10, price=10,
                                                is_tax_included=True, tax_name='Redusa', tax_percentage=9,
                                                is_service=True)
        client = self.smartbill.create_client(name_client='test', country_client="Romania")
        invoice = self.smartbill.create_invoice(client, [product, product2], issue_date="2018-05-01")
        self.assertEqual(invoice['series'], 'C')
        self.assertEqual(invoice['errorText'], '')

    def test_create_invoice_product_no_stock(self):
        product = self.smartbill.create_product(name_product='Capsator', code='MK001',
                                                measuring_unit_name='buc', quantify=10, price=10,
                                                is_tax_included=True, tax_name='Redusa', tax_percentage=9,
                                                is_service=False, use_stock=True, ware_house_name='Amazon2')
        product2 = self.smartbill.create_product(name_product='Service name', code='test',
                                                measuring_unit_name='h', quantify=10, price=10,
                                                is_tax_included=True, tax_name='Redusa', tax_percentage=9,
                                                is_service=True)
        client = self.smartbill.create_client(name_client='test', country_client="Romania")
        invoice = self.smartbill.create_invoice(client, [product, product2], issue_date="2018-05-01")
        self.assertNotEqual(invoice['errorText'], '')
