from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Product
from app.domain.user_models import User


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

class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    @abstractmethod
    def create(self, user: User) -> User:
        pass
