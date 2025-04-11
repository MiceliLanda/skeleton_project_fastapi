from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class UserCredentials(SQLModel, table = True):
    # Atributos
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(nullable=False, min_length=6, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relación inversa
    user:Optional['User'] = Relationship(back_populates='credentials')