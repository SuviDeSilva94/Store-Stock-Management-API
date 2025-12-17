from datetime import timedelta
from typing import Optional
from app.domain.user_models import User
from app.infrastructure.user_repository import UserRepository
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.core.exceptions import ApplicationError


class AuthenticationError(ApplicationError):
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(message)


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already exists")


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.user_repository.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_user(self, username: str, email: str, password: str) -> User:
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            raise UserAlreadyExistsError(username)
        
        existing_email = self.user_repository.get_by_email(email)
        if existing_email:
            raise ApplicationError(f"Email '{email}' already registered")
        
        hashed_password = get_password_hash(password)
        user = User(
            id=None,
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=True
        )
        return self.user_repository.create(user)
    
    def create_access_token_for_user(self, user: User) -> str:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        return access_token

