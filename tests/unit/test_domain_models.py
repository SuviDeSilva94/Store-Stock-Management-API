import pytest
from app.domain.models import Product
from app.core.exceptions import InvalidAmountError, InsufficientStockError
class TestProductDomainModel:
    def test_create_product(self):
        product = Product(
            id=1,
            name="Test Product",
            sku="TEST-001",
            stock=10
        )
        assert product.id == 1
        assert product.name == "Test Product"
        assert product.sku == "TEST-001"
        assert product.stock == 10
    def test_increment_stock_success(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=10)
        product.increment_stock(5)
        assert product.stock == 15
    def test_increment_stock_with_zero_raises_error(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=10)
        with pytest.raises(InvalidAmountError) as exc_info:
            product.increment_stock(0)
        assert "must be positive" in str(exc_info.value)
    def test_increment_stock_with_negative_raises_error(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=10)
        with pytest.raises(InvalidAmountError):
            product.increment_stock(-5)
    def test_decrement_stock_success(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=10)
        product.decrement_stock(3)
        assert product.stock == 7
    def test_decrement_stock_to_zero(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=5)
        product.decrement_stock(5)
        assert product.stock == 0
    def test_decrement_stock_below_zero_raises_error(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=5)
        with pytest.raises(InsufficientStockError) as exc_info:
            product.decrement_stock(10)
        error = exc_info.value
        assert error.current_stock == 5
        assert error.requested_amount == 10
    def test_decrement_stock_with_zero_raises_error(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=10)
        with pytest.raises(InvalidAmountError):
            product.decrement_stock(0)
    def test_is_in_stock_true(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=5)
        assert product.is_in_stock() is True
    def test_is_in_stock_false(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=0)
        assert product.is_in_stock() is False
    def test_is_low_stock(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=5)
        assert product.is_low_stock(threshold=10) is True
        assert product.is_low_stock(threshold=3) is False
    def test_update_details(self):
        product = Product(id=1, name="Old Name", sku="TEST-001", stock=10)
        product.update_details(name="New Name", stock=20)
        assert product.name == "New Name"
        assert product.stock == 20
    def test_update_details_partial(self):
        product = Product(id=1, name="Old Name", sku="TEST-001", stock=10)
        product.update_details(name="New Name")
        assert product.name == "New Name"
        assert product.stock == 10
    def test_update_details_negative_stock_raises_error(self):
        product = Product(id=1, name="Test", sku="TEST-001", stock=10)
        with pytest.raises(InvalidAmountError):
            product.update_details(stock=-5)
