from inventory.exceptions import InvalidDataError
from datetime import date
class Product:
    def __init__(self, sku, name, price, qty):
        if price <=0 or qty <0: raise InvalidDataError("Invalid")
        self._sku=sku; self._name=name; self._price=price; self._qty=qty
    def get_value(self): return self._price*self._qty
    def to_dict(self): return {"type":"base","sku":self._sku,"name":self._name,"price":self._price,"qty":self._qty}
    @property
    def sku(self): return self._sku
class PerishableProduct(Product):
    def __init__(self, sku, name, price, qty, expiry):
        super().__init__(sku,name,price,qty)
        self.expiry=expiry
    def get_value(self):
        return super().get_value()*0.8 if self.expiry < date.today() else super().get_value()
    def to_dict(self):
        d=super().to_dict(); d.update({"type":"perishable","expiry":self.expiry.isoformat()}); return d
class ElectronicProduct(Product):
    def __init__(self, sku, name, price, qty, warranty_months):
        super().__init__(sku,name,price,qty)
        self.warranty=warranty_months
    def get_value(self): return super().get_value()*1.1
    def to_dict(self):
        d=super().to_dict(); d.update({"type":"electronic","warranty":self.warranty}); return d
