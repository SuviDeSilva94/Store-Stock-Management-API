from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.domain.interfaces import IProductRepository
from app.domain.models import Product
from app.infrastructure.db_models import ProductModel
from app.core.exceptions import DuplicateSKUError


class SQLAlchemyProductRepository(IProductRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, product: Product) -> Product:
        try:
            db_product = ProductModel(
                name=product.name,
                sku=product.sku,
                stock=product.stock
            )
            
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            
            return self._to_domain(db_product)
            
        except IntegrityError:
            self.db.rollback()
            raise DuplicateSKUError(product.sku)
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        db_product = self.db.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        
        return self._to_domain(db_product) if db_product else None
    
    def get_by_sku(self, sku: str) -> Optional[Product]:
        db_product = self.db.query(ProductModel).filter(
            ProductModel.sku == sku
        ).first()
        
        return self._to_domain(db_product) if db_product else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        db_products = self.db.query(ProductModel)\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        return [self._to_domain(p) for p in db_products]
    
    def update(self, product: Product) -> Product:
        db_product = self.db.query(ProductModel).filter(
            ProductModel.id == product.id
        ).first()
        
        if db_product:
            db_product.name = product.name
            db_product.stock = product.stock
            
            self.db.commit()
            self.db.refresh(db_product)
            
            return self._to_domain(db_product)
        
        return product
    
    def delete(self, product_id: int) -> bool:
        db_product = self.db.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
            return True
        
        return False
    
    def _to_domain(self, db_product: ProductModel) -> Product:
        return Product(
            id=db_product.id,
            name=db_product.name,
            sku=db_product.sku,
            stock=db_product.stock,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at
        )
