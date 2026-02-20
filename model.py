# model.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

#schemas to validate incoming data from client side 

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    class config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
   

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


#schemas to validate user when user need to signup

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length = 8, max_length=64)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length = 8, max_length=64)


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True




