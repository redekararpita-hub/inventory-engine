class InventoryError(Exception): pass
class InvalidDataError(InventoryError): pass
class InsufficientStockError(InventoryError): pass
class ProductNotFoundError(InventoryError): pass
