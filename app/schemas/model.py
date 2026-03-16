# model.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

#schemas to validate incoming data from admin or staff side 

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



#schemas to validate incoming data from user or client side for their cart operations

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)

class CartItemResponse(BaseModel):
    product_id: int
    product_name: str
    price: float
    quantity: int
    total_price: float
    in_stock: bool

class CartResponse(BaseModel):
    items: list[CartItemResponse]
    cart_total: float