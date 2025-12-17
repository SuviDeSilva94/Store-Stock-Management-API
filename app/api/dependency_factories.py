from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories import SQLAlchemyProductRepository
from app.infrastructure.user_repository import UserRepository
from app.domain.interfaces import IProductRepository
from app.domain.services import ProductService
from app.domain.auth_service import AuthService
from app.domain.user_models import User
from app.core.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_product_repository(
    db: Session = Depends(get_db)
) -> IProductRepository:
    return SQLAlchemyProductRepository(db)


def get_product_service(
    repository: IProductRepository = Depends(get_product_repository)
) -> ProductService:
    return ProductService(repository)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(user_repository)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = user_repository.get_by_username(username)
    if user is None:
        raise credentials_exception
    
    return user


__all__ = [
    "get_db",
    "get_product_repository",
    "get_product_service",
    "get_user_repository",
    "get_auth_service",
    "get_current_user",
    "Depends"
]

