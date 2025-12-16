from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Product


class IProductRepository(ABC):
    @abstractmethod
    def create(self, product: Product) -> Product:
        pass
    
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass
    
    @abstractmethod
    def get_by_sku(self, sku: str) -> Optional[Product]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        pass
    
    @abstractmethod
    def update(self, product: Product) -> Product:
        pass
    
    @abstractmethod
    def delete(self, product_id: int) -> bool:
        pass
