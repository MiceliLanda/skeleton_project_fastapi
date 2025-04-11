from datetime import datetime
from typing import List, Optional
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel
from .user_permissions import UserPermissions

try:
    from src.schemas.security import UserRole
except ImportError:
    from schemas.security import UserRole
    
class User(SQLModel, table = True):
    # Atributos
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=5, max_length=50)
    email: str = Field(unique=True, index=True, nullable=False)
    status: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    roles: List[UserRole] = Field(default_factory=lambda: [UserRole.CLIENT], sa_type=JSON())
    
    # Relaciones
    
    # (1:1 con UserCredentials)
    credentials: Optional["UserCredentials"] = Relationship(
        back_populates="user"
    )
    # (m:m con UserCredentials) que es una tabla de asociación
    permissions: List["Permissions"] = Relationship(
        back_populates="users",
        link_model=UserPermissions
    )