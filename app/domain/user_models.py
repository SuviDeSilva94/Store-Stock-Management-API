from typing import Optional
from datetime import datetime


class User:
    def __init__(
        self,
        id: Optional[int],
        username: str,
        email: str,
        hashed_password: str,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = id
        self._username = username
        self._email = email
        self._hashed_password = hashed_password
        self._is_active = is_active
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def hashed_password(self) -> str:
        return self._hashed_password
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"

