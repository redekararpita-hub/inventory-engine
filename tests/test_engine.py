import json, csv, os
from datetime import date, timedelta
from inventory.models import Product, PerishableProduct, ElectronicProduct
from inventory.engine import InventoryEngine
from inventory.exceptions import InvalidDataError

def test_inheritance_polymorphism():
    p1 = Product("A1","Pen",10,5)
    p2 = PerishableProduct("P1","Milk",10,5, date.today()+timedelta(days=2))
    p3 = ElectronicProduct("E1","Phone",100,1,12)
    assert p1.get_value()==50
    assert abs(p3.get_value()-110) < 0.01

def test_custom_exceptions():
    try:
        Product("X","Bad",-5,1)
        assert False
    except InvalidDataError:
        pass

def test_engine_stock():
    eng=InventoryEngine()
    eng.add_product(Product("A1","Pen",10,5))
    eng.remove_stock("A1",2)
    assert eng._products["A1"]._qty==3

def test_json_persistence():
    eng=InventoryEngine()
    eng.add_product(Product("A1","Pen",10,5))
    eng.save_json("data/temp.json")
    eng2=InventoryEngine()
    eng2.load_json("data/temp.json")
    assert eng2.get_total_value()==50

def test_csv_persistence():
    eng=InventoryEngine()
    eng.add_product(Product("A1","Pen",10,5))
    eng.save_csv("data/temp.csv")
    assert os.path.exists("data/temp.csv")

def test_basic():
    eng=InventoryEngine()
    eng.add_product(Product("A1","Pen",10,5))
    assert eng.get_total_value()==50
