# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from model import ProductCreate, ProductUpdate, ProductResponse, UserCreate, UserResponse, UserLogin
from database import session, engine
import database_models 
from sqlalchemy.orm import Session
from typing import List
import security
import auth
from decodingtokens import get_current_user, oauth2_scheme
from jose import jwt
from datetime import datetime, timezone

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)


database_models.Base.metadata.create_all(bind = engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# Signup endpoint for user
@app.post("/signup", status_code=201, response_model = UserResponse)
def sign_up(user: UserCreate,db : Session = Depends(get_db)):
    email = user.email.lower()

    existing_user = db.query(database_models.User).filter(database_models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already Exists")
    
    hashed_password = security.get_password_hash(user.password)

    db_user = database_models.User(
        email = email,
        hashed_password = hashed_password,
        is_active = True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#login endpoint for user
@app.post("/login", status_code=200,)
def login(user: UserLogin,db : Session = Depends(get_db) ):
    email = user.email.lower()

    db_user = db.query(database_models.User).filter(database_models.User.email == email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="inactive user")
    
    access_token = auth.create_access_token(
        data={ "sub" : db_user.email, "user_id" : db_user.user_id }
    )

    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }


#logout endpoint for user
@app.post("/logout",status_code=status.HTTP_200_OK)
def logout(token: str = Depends(oauth2_scheme),current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    payload = jwt.decode(
        token, auth.secret_key, algorithms=[auth.ALGORITHM]
        )
    
    exp_timestamp = payload.get("exp")
    if exp_timestamp is None:
        raise HTTPException(status_code=400, detail="Invalid token")

    expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

    existing = db.query(database_models.RevokedToken).filter(database_models.RevokedToken.token == token).first()

    if not existing:
        db_user = database_models.RevokedToken(
        token = token,
        user_id = current_user.user_id,
        revoked_at = datetime.now(timezone.utc),
        expires_at = expires_at
        )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "{message}: {Logout Successfully Done}"





# GET all products
@app.get("/products", response_model=List[ProductResponse])
def get_all_products(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()


# GET product by id
@app.get("/products/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    db_product_by_id = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product_by_id:
        return db_product_by_id

    raise HTTPException(status_code=404, detail="Product not found")


# POST create product
@app.post("/products", status_code=201,response_model=ProductResponse)
def create_product(product: ProductCreate,current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    
    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)

    db.commit()
    db.refresh(db_product)
    return db_product


# PUT replace product (full update)
@app.put("/products/{id}", response_model = ProductResponse)
def replace_product(id: int, product: ProductCreate,current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    db_product_by_id = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product_by_id:
        db_product_by_id.name = product.name
        db_product_by_id.description = product.description
        db_product_by_id.price = product.price
        db_product_by_id.quantity = product.quantity
        db.commit()
        db.refresh(db_product_by_id)
        return db_product_by_id
    
    raise HTTPException(status_code=404, detail="Product not found")



# DELETE product
@app.delete("/products/{id}", current_user = Depends(get_current_user), status_code=204)
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return 
    
    raise HTTPException(status_code=404, detail="Product not found")

# PATCH update product (partial update)
@app.patch("/products/{id}", current_user = Depends(get_current_user), response_model=ProductResponse)
def update_product(id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        if product_update.name is not None:
            db_product.name = product_update.name
        if product_update.description is not None:
            db_product.description = product_update.description
        if product_update.price is not None:
            db_product.price = product_update.price
        if product_update.quantity is not None:
            db_product.quantity = product_update.quantity
        db.commit()
        db.refresh(db_product)
        return db_product
    
    raise HTTPException(status_code=404, detail="Product not found")