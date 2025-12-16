import pytest
from unittest.mock import Mock, MagicMock
from app.domain.services import ProductService
from app.domain.interfaces import IProductRepository
from app.domain.models import Product
from app.core.exceptions import (
    ProductNotFoundError,
    DuplicateSKUError,
    InvalidAmountError,
    InsufficientStockError
)
@pytest.fixture
def mock_repository():
    return Mock(spec=IProductRepository)
@pytest.fixture
def service(mock_repository):
    return ProductService(mock_repository)
@pytest.fixture
def sample_product():
    return Product(
        id=1,
        name="Test Product",
        sku="TEST-001",
        stock=10
    )
class TestProductService:
    def test_create_product_success(self, service, mock_repository, sample_product):
        mock_repository.get_by_sku.return_value = None
        mock_repository.create.return_value = sample_product
        product = service.create_product(
            name="Test Product",
            sku="test-001",
            stock=10
        )
        assert product.id is not None
        assert product.name == "Test Product"
        assert product.sku == "TEST-001"
        mock_repository.create.assert_called_once()
    def test_create_product_normalizes_sku(self, service, mock_repository, sample_product):
        mock_repository.get_by_sku.return_value = None
        mock_repository.create.return_value = sample_product
        product = service.create_product(
            name="Test Product",
            sku="test-001",
            stock=10
        )
        assert product.sku == "TEST-001"
    def test_create_product_with_duplicate_sku_raises_error(self, service, mock_repository, sample_product):
        mock_repository.get_by_sku.return_value = sample_product
        with pytest.raises(DuplicateSKUError) as exc_info:
            service.create_product(name="Product 2", sku="TEST-001", stock=5)
        assert "TEST-001" in str(exc_info.value)
    def test_create_product_with_empty_name_raises_error(self, service, mock_repository):
        with pytest.raises(InvalidAmountError):
            service.create_product(name="", sku="TEST-001", stock=10)
    def test_create_product_with_negative_stock_raises_error(self, service, mock_repository):
        with pytest.raises(InvalidAmountError):
            service.create_product(name="Test", sku="TEST-001", stock=-5)
    def test_get_product_by_id_success(self, service, mock_repository, sample_product):
        mock_repository.get_by_id.return_value = sample_product
        retrieved = service.get_product_by_id(1)
        assert retrieved.id == sample_product.id
        assert retrieved.name == sample_product.name
        mock_repository.get_by_id.assert_called_once_with(1)
    def test_get_product_by_id_not_found_raises_error(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None
        with pytest.raises(ProductNotFoundError) as exc_info:
            service.get_product_by_id(999)
        assert exc_info.value.product_id == 999
    def test_get_all_products(self, service, mock_repository, sample_product):
        product2 = Product(id=2, name="Product 2", sku="TEST-002", stock=20)
        mock_repository.get_all.return_value = [sample_product, product2]
        products = service.get_all_products()
        assert len(products) == 2
        mock_repository.get_all.assert_called_once_with(skip=0, limit=100)
    def test_get_all_products_with_pagination(self, service, mock_repository):
        mock_repository.get_all.return_value = []
        service.get_all_products(skip=1, limit=2)
        mock_repository.get_all.assert_called_once_with(skip=1, limit=2)
    def test_update_product_success(self, service, mock_repository, sample_product):
        updated_product = Product(id=1, name="New Name", sku="TEST-001", stock=20)
        mock_repository.get_by_id.return_value = sample_product
        mock_repository.update.return_value = updated_product
        updated = service.update_product(
            product_id=1,
            name="New Name",
            stock=20
        )
        assert updated.name == "New Name"
        assert updated.stock == 20
        mock_repository.update.assert_called_once()
    def test_update_product_partial(self, service, mock_repository, sample_product):
        updated_product = Product(id=1, name="New Name", sku="TEST-001", stock=10)
        mock_repository.get_by_id.return_value = sample_product
        mock_repository.update.return_value = updated_product
        updated = service.update_product(product_id=1, name="New Name")
        assert updated.name == "New Name"
        assert updated.stock == 10
    def test_update_product_not_found_raises_error(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None
        with pytest.raises(ProductNotFoundError):
            service.update_product(product_id=999, name="Test")
    def test_delete_product_success(self, service, mock_repository, sample_product):
        mock_repository.get_by_id.return_value = sample_product
        mock_repository.delete.return_value = True
        service.delete_product(1)
        mock_repository.delete.assert_called_once_with(1)
    def test_delete_product_not_found_raises_error(self, service, mock_repository):
        mock_repository.get_by_id.return_value = None
        with pytest.raises(ProductNotFoundError):
            service.delete_product(999)
    def test_increment_stock_success(self, service, mock_repository, sample_product):
        mock_repository.get_by_id.return_value = sample_product
        updated_product = Product(id=1, name="Test Product", sku="TEST-001", stock=15)
        mock_repository.update.return_value = updated_product
        updated = service.increment_stock(1, amount=5)
        assert updated.stock == 15
        mock_repository.update.assert_called_once()
    def test_increment_stock_default_amount(self, service, mock_repository, sample_product):
        mock_repository.get_by_id.return_value = sample_product
        updated_product = Product(id=1, name="Test Product", sku="TEST-001", stock=11)
        mock_repository.update.return_value = updated_product
        updated = service.increment_stock(1)
        assert updated.stock == 11
    def test_increment_stock_invalid_amount_raises_error(self, service, mock_repository, sample_product):
        mock_repository.get_by_id.return_value = sample_product
        with pytest.raises(InvalidAmountError):
            service.increment_stock(1, amount=0)
    def test_decrement_stock_success(self, service, mock_repository, sample_product):
        mock_repository.get_by_id.return_value = sample_product
        updated_product = Product(id=1, name="Test Product", sku="TEST-001", stock=7)
        mock_repository.update.return_value = updated_product
        updated = service.decrement_stock(1, amount=3)
        assert updated.stock == 7
        mock_repository.update.assert_called_once()
    def test_decrement_stock_insufficient_raises_error(self, service, mock_repository):
        product = Product(id=1, name="Test Product", sku="TEST-001", stock=5)
        mock_repository.get_by_id.return_value = product
        with pytest.raises(InsufficientStockError) as exc_info:
            service.decrement_stock(1, amount=10)
        error = exc_info.value
        assert error.current_stock == 5
        assert error.requested_amount == 10
