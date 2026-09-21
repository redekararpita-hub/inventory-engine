import json, csv
from inventory.models import Product, PerishableProduct, ElectronicProduct
from inventory.exceptions import ProductNotFoundError, InsufficientStockError
from datetime import date
class InventoryEngine:
    def __init__(self): self._products={}
    def add_product(self, p): self._products[p.sku]=p
    def remove_stock(self, sku, n):
        if sku not in self._products: raise ProductNotFoundError(sku)
        if self._products[sku]._qty < n: raise InsufficientStockError("low")
        self._products[sku]._qty-=n
    def save_json(self, path):
        with open(path,'w') as f: json.dump([p.to_dict() for p in self._products.values()],f,indent=2)
    def load_json(self, path):
        with open(path) as f: data=json.load(f)
        for d in data:
            if d['type']=='perishable': p=PerishableProduct(d['sku'],d['name'],d['price'],d['qty'],date.fromisoformat(d['expiry']))
            elif d['type']=='electronic': p=ElectronicProduct(d['sku'],d['name'],d['price'],d['qty'],d['warranty'])
            else: p=Product(d['sku'],d['name'],d['price'],d['qty'])
            self.add_product(p)
    def save_csv(self, path):
        with open(path,'w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=["sku","name","price","qty"]); w.writeheader()
            for p in self._products.values(): w.writerow({"sku":p._sku,"name":p._name,"price":p._price,"qty":p._qty})
    def get_total_value(self): return sum(p.get_value() for p in self._products.values())
