from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from .user_permissions import UserPermissions

class Permissions(SQLModel, table = True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name:str = Field(nullable=False)
    prefix: str = Field(nullable=False)
    module: str = Field(nullable=False)
    status: bool = Field(default=True)
    
    # Relación (m:m) con user
    users: List["User"] = Relationship(
        back_populates='permissions',
        link_model=UserPermissions
    )
    