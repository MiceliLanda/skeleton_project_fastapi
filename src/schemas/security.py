from pydantic import BaseModel
from .user import UserLoginResponse
from enum import Enum

class TokenData(BaseModel):
    username: str | None = None
    
class Token(BaseModel):
    token: str
    user: UserLoginResponse
      
class LoginRequest(BaseModel):
    username: str
    password: str
    
class UserRole( str, Enum):
    ADMIN = "admin"
    CLIENT = "client"