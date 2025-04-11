from datetime import datetime
from typing import List
from pydantic import EmailStr, constr
from sqlmodel import SQLModel

class User(SQLModel):
    id: int
    username: str
    password: str
    email: str | None = None
    created_at: datetime
    status : bool

class UserLoginResponse(SQLModel):
    id: int
    username: str
    email: str | None = None
    created_at: datetime
    status : bool
    roles: List[str]
    
class UserResponse(SQLModel):
    id: int
    username: str
    email: str | None = None
    created_at: datetime
    status : bool
    roles: List[str]

class UserCreate(SQLModel):
    username: constr(min_length=5, max_length=20) # type: ignore
    password: constr(min_length=8, max_length=50) # type: ignore
    email: EmailStr
    
class UserAddPermissions(SQLModel):
    permissions_ids: List[int]
    
class UserListResponse(SQLModel):
    users: List[UserResponse]
