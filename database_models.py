from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Product(Base):

    __tablename__ = "Product"

    id = Column(Integer, primary_key = True, index = True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)



class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key = True, autoincrement= True)
    email = Column(String, unique= True, index=True)
    hashed_password = Column(String, nullable = False)
    is_active = Column(Boolean, default=True)

class RevokedToken(Base):

    __tablename__ = "revoked_token"
    id = Column(Integer, nullable=False, primary_key=True, index=True, autoincrement= True)
    token = Column(String, nullable=False, index=True)
    user_id = Column(Integer, nullable=False)
    revoked_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)