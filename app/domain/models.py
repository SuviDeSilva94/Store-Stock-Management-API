from datetime import datetime
from typing import Optional
from app.core.exceptions import InsufficientStockError, InvalidAmountError


class Product:
    def __init__(
        self,
        id: Optional[int],
        name: str,
        sku: str,
        stock: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = id
        self._name = name
        self._sku = sku
        self._stock = stock
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def sku(self) -> str:
        return self._sku
    
    @property
    def stock(self) -> int:
        return self._stock
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def increment_stock(self, amount: int) -> None:
        if amount <= 0:
            raise InvalidAmountError(
                amount, 
                "Increment amount must be positive"
            )
        
        self._stock += amount
        self._updated_at = datetime.utcnow()
    
    def decrement_stock(self, amount: int) -> None:
        if amount <= 0:
            raise InvalidAmountError(
                amount,
                "Decrement amount must be positive"
            )
        
        if self._stock - amount < 0:
            raise InsufficientStockError(self._stock, amount)
        
        self._stock -= amount
        self._updated_at = datetime.utcnow()
    
    def update_details(self, name: Optional[str] = None, stock: Optional[int] = None) -> None:
        if name is not None:
            self._name = name
        
        if stock is not None:
            if stock < 0:
                raise InvalidAmountError(stock, "Stock cannot be negative")
            self._stock = stock
        
        self._updated_at = datetime.utcnow()
    
    def is_in_stock(self) -> bool:
        return self._stock > 0
    
    def is_low_stock(self, threshold: int = 10) -> bool:
        return self._stock < threshold
    
    def __repr__(self) -> str:
        return (
            f"Product(id={self._id}, name='{self._name}', "
            f"sku='{self._sku}', stock={self._stock})"
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return False
        return self._id == other._id and self._sku == other._sku
