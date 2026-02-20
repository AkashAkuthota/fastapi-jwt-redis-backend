from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Product(Base):

    __tablename__ = "product"

    id = Column(Integer, primary_key = True, index = True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)



class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key = True, autoincrement= True)
    email = Column(String, unique= True, index=True)
    hashed_password = Column(String, nullable = False)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)

class RevokedToken(Base):

    __tablename__ = "revoked_token"
    id = Column(Integer, nullable=False, primary_key=True, index=True, autoincrement= True)
    token = Column(String, nullable=False, index=True, unique=True)
    user_id = Column(Integer, nullable=False)
    revoked_at = Column(DateTime(timezone=True),index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True),index=True, nullable=False)


class Refresh_Tokens(Base):

    __tablename__ = "refresh_tokens"

    id = Column(Integer, nullable= False, primary_key=True, index= True, autoincrement=True)
    token = Column(String, nullable=False, unique=True, index = True)
    user_id = Column(Integer, nullable=False)

    expires_at = Column(DateTime(timezone=True),index=True, nullable=False)
    revoked_at = Column(DateTime(timezone=True),index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)

    replaced_by_token = Column(String, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
