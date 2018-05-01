from .authenticate import AuthenticateMixin
from .invoice import InvoiceSmartBill
from .config import ConfigSmartBill


class SmartBill(InvoiceSmartBill, AuthenticateMixin, ConfigSmartBill,):
    base_url = 'https://ws.smartbill.ro:8183/SBORO/api'

    def __init__(self, smartbill_user, smartbill_token, smartbill_ciff,
                 currency='RON', language='RO', saveToD=False, useStock=False):
        self.smartbill_user = smartbill_user
        self.smartbill_token = smartbill_token
        self.smartbill_ciff = smartbill_ciff
        self.parrams = {'cif': self.smartbill_ciff}
        self.currency = currency
        self.language = language
        self.saveToD = saveToD
        self.useStock = useStock
        super().__init__()
