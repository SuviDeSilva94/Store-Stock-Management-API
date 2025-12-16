from typing import List, Optional
from app.domain.models import Product
from app.domain.interfaces import IProductRepository
from app.core.exceptions import (
    ProductNotFoundError,
    DuplicateSKUError,
    InvalidAmountError,
    InsufficientStockError
)


class ProductService:
    def __init__(self, repository: IProductRepository):
        self.repository = repository
    
    def create_product(
        self, 
        name: str, 
        sku: str, 
        stock: int = 0
    ) -> Product:
        if not name or not name.strip():
            raise InvalidAmountError(0, "Product name cannot be empty")
        
        if not sku or not sku.strip():
            raise InvalidAmountError(0, "Product SKU cannot be empty")
        
        if stock < 0:
            raise InvalidAmountError(stock, "Initial stock cannot be negative")
        
        existing = self.repository.get_by_sku(sku)
        if existing:
            raise DuplicateSKUError(sku)
        
        product = Product(
            id=None,
            name=name.strip(),
            sku=sku.strip().upper(),
            stock=stock
        )
        
        return self.repository.create(product)
    
    def get_product_by_id(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        
        if not product:
            raise ProductNotFoundError(product_id)
        
        return product
    
    def get_all_products(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        return self.repository.get_all(skip=skip, limit=limit)
    
    def update_product(
        self,
        product_id: int,
        name: Optional[str] = None,
        stock: Optional[int] = None
    ) -> Product:
        product = self.get_product_by_id(product_id)
        
        if name is not None and (not name or not name.strip()):
            raise InvalidAmountError(0, "Product name cannot be empty")
        
        if stock is not None and stock < 0:
            raise InvalidAmountError(stock, "Stock cannot be negative")
        
        product.update_details(
            name=name.strip() if name else None,
            stock=stock
        )
        
        return self.repository.update(product)
    
    def delete_product(self, product_id: int) -> None:
        product = self.get_product_by_id(product_id)
        self.repository.delete(product.id)
    
    def increment_stock(
        self, 
        product_id: int, 
        amount: int = 1
    ) -> Product:
        product = self.get_product_by_id(product_id)
        product.increment_stock(amount)
        return self.repository.update(product)
    
    def decrement_stock(
        self, 
        product_id: int, 
        amount: int = 1
    ) -> Product:
        product = self.get_product_by_id(product_id)
        product.decrement_stock(amount)
        return self.repository.update(product)
