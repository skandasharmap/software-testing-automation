import pytest

from services.product_service.main import ProductIn


def test_product_validation():
    p = ProductIn(name="Pen", price=10.0, stock=5)
    assert p.name == "Pen"
    assert p.stock == 5
    with pytest.raises(Exception):
        ProductIn(name="A", price=-1.0, stock=-5)
