from typing import Optional
from sqlalchemy.orm import Session
from app.domain.user_models import User
from app.infrastructure.db_models import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def _to_domain(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    
    def _to_db_model(self, user: User) -> UserModel:
        return UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
    def get_by_username(self, username: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(
            UserModel.username == username
        ).first()
        return self._to_domain(db_user) if db_user else None
    
    def get_by_email(self, email: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(
            UserModel.email == email
        ).first()
        return self._to_domain(db_user) if db_user else None
    
    def create(self, user: User) -> User:
        db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_domain(db_user)

