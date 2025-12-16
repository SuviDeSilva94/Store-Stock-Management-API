from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories import SQLAlchemyProductRepository
from app.domain.interfaces import IProductRepository
from app.domain.services import ProductService


def get_product_repository(
    db: Session = Depends(get_db)
) -> IProductRepository:
    return SQLAlchemyProductRepository(db)


def get_product_service(
    repository: IProductRepository = Depends(get_product_repository)
) -> ProductService:
    return ProductService(repository)


__all__ = ["get_db", "get_product_repository", "get_product_service", "Depends"]

