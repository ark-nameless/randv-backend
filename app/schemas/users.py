from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class UserInfo(BaseModel):
    username: str
    email: str
    access: List
    is_active: bool


class RegisterUser(BaseModel):
    username: str = Field(..., description="user username")
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=32, description="user password")
    access: List[str] = Field(..., description="user access control")

# class UserModel(BaseModel):
#     id: int = Field(..., description="user id")
#     username: str = Field(..., description="user username")
#     email: str = Field(..., description="user email")
#     password: str = Field(..., min_length=5, max_length=32, description="user password")
#     access: list = Field(..., description="user access control")
#     is_active: bool = Field(..., description="user acccount is still active")
#     reset_token: str = Field(..., description="password reset token")

class UserModel(BaseModel):
    id: int
    username: str
    email: str
    password: str
    access: List
    is_active: bool
    reset_token: str

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=32, description="user password")
    

class UserOut(BaseModel):
    id: UUID
    email: str


class SystemUser(UserOut):
    password: str