import json
import requests

class InvoiceSmartBill(object):

    def create_client(self, name_client, country_client, vat_code_client=None, is_tax_payer_client=None,
                      address_client=None, city_client=None, email_client=None, save_to_db_client=False):
        return {"name": name_client,
                "vatCode": vat_code_client,
                "isTaxPayer": is_tax_payer_client,
                "address": address_client,
                "city": city_client,
                "country": country_client,
                "email": email_client,
                "saveToDb": save_to_db_client
                }

    def create_product(self, name_product, code, measuring_unit_name, quantify, price,
                       is_tax_included, tax_name, tax_percentage, is_service, currency=None, is_discount=False,
                       save_to_db_product=False, use_stock=False, ware_house_name=None):

        if not currency:
            currency = self.currency

        product = {"name": name_product,
                   "isDiscount": is_discount,
                   "code": code,
                   "measuringUnitName": measuring_unit_name,
                   "currency": currency,
                   "quantity": quantify,
                   "price": price,
                   "isTaxIncluded": is_tax_included,
                   "taxName": tax_name,
                   "taxPercentage": tax_percentage,
                   "isService": is_service,
                   "saveToDb": save_to_db_product
                   }
        if not is_service:
            if use_stock:
                product.update({'warehouseName':ware_house_name})
        return product

    def create_invoice(self, client, products, issue_date, series_number=None, is_draft=False, due_date=None,
                       delivery_date=None):

        if not series_number:
            series_number = self.get_series()['list'][0]['name']

        data = {"companyVatCode": self.smartbill_ciff,
                "client": client,
                "issueDate": issue_date,
                "seriesName": series_number,
                "isDraft": is_draft,
                "dueDate": due_date,
                "deliveryDate": delivery_date,
                "products": products,
                'useStock': True,
              }
        data = json.dumps(data)
        response = requests.post(f"{self.base_url}/invoice", headers=self.headers, data=data)
        return response.json()
