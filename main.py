# main.py
from fastapi import FastAPI, HTTPException, Depends, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from token_cleanup import cleanup_tokens
from model import ProductCreate, ProductUpdate, ProductResponse, UserCreate, UserResponse, UserLogin
from database import engine, get_db
import database_models
from sqlalchemy.orm import Session
from typing import List
import security
import auth
from decodingtokens import get_current_user
from datetime import datetime, timezone, timedelta
from auth_context import AuthContext
from permissions import require_role
from redis_client import redis_client, blacklist_token
from rate_limiter import check_login_rate_limits, check_refresh_rate_limit







@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_tokens, 'interval',minutes = 10)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)


database_models.Base.metadata.create_all(bind = engine)



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
@app.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLogin,request : Request, response : Response, db : Session = Depends(get_db) ):
    
    email = user.email.lower()
    
    client_ip = request.client.host
    check_login_rate_limits(client_ip, email)

    db_user = db.query(database_models.User).filter(database_models.User.email == email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

    if not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="inactive user")
    
    redis_client.delete(f"login:ip:{client_ip}")
    redis_client.delete(f"login:email:{email}")

    access_token = auth.create_access_token(
        data={ "sub" : db_user.email, "user_id" : db_user.user_id }
    )
    refresh_token = auth.create_refresh_token()
    
    now = datetime.now(timezone.utc)
    
    expires_at = now + timedelta(days = auth.REFRESH_TOKEN_EXPIRE_DAYS)

    db_refresh_token = database_models.Refresh_Tokens(
        token =  refresh_token,
        user_id = db_user.user_id,
        expires_at = expires_at,
        revoked_at = None,
        created_at = now,
        replaced_by_token = None,
        last_used_at = None,
    )

    db.add(db_refresh_token)
    db.commit()
    db.refresh(db_refresh_token)
    
    response.set_cookie(
        key = "refresh_token",
        value = refresh_token,
        httponly=True,
        secure=False, #Because of localhost
        samesite="lax",
        max_age= (auth.REFRESH_TOKEN_EXPIRE_DAYS) * 24 * 60 * 60
    )
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }



#refresh_token endpoint for frontend
@app.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_token(request : Request, response : Response, db : Session = Depends(get_db)):
    incoming_token = request.cookies.get("refresh_token")

    if incoming_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh Token Missing")
    
    db_refresh_token = db.query(database_models.Refresh_Tokens).filter(database_models.Refresh_Tokens.token == incoming_token).first()

    if not db_refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    now = datetime.now(timezone.utc)
    if db_refresh_token.expires_at <= now:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token is expired")
    
    user = db.query(database_models.User).filter(database_models.User.user_id == db_refresh_token.user_id).first()

    if user is None or not user.is_active : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user invalid")
    
    client_ip = request.client.host
    user_id = db_refresh_token.user_id
    check_refresh_rate_limit(client_ip,user_id)

    if db_refresh_token.revoked_at is not None:
        active_tokens = db.query(database_models.Refresh_Tokens).filter(
            database_models.Refresh_Tokens.user_id == db_refresh_token.user_id, 
            database_models.Refresh_Tokens.revoked_at == None
            ).all()

        for token in active_tokens:
            token.revoked_at = now
            token.replaced_by_token = "BREACH_DETECTED"
            token.last_used_at = now

        db.commit()
        response.delete_cookie(
            key="refresh_token",
            httponly=True
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Security breach detected. All sessions invalidated")

    new_refresh_token = auth.create_refresh_token()
    new_expiry = now + timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)

    updated = db.query(database_models.Refresh_Tokens).filter(
        database_models.Refresh_Tokens.token == incoming_token,
        database_models.Refresh_Tokens.revoked_at == None
        ).update({
            "revoked_at" : now,
            "replaced_by_token":new_refresh_token,
            "last_used_at": now
        })
    if updated == 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token  already used")


    new_db_refresh = database_models.Refresh_Tokens(
    token = new_refresh_token,
    user_id = user.user_id,
    expires_at = new_expiry,
    created_at = now,
    replaced_by_token = None,
    revoked_at = None,
    last_used_at = None,
    )
        
    db.add(new_db_refresh)
    db.commit()
    db.refresh(new_db_refresh)

        
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,  #Because of localhost
        samesite="lax",
        max_age= int(auth.REFRESH_TOKEN_EXPIRE_DAYS) * 24 * 60 * 60
    )
    access_token = auth.create_access_token(
        data = {"sub" : user.email, "user_id" : user.user_id}
    )

    return {
        "access_token" : access_token,
        "token_type" : "bearer"    
    }




#logout endpoint for user
@app.post("/logout",status_code=status.HTTP_200_OK)
def logout(request: Request,response: Response, current_user: AuthContext = Depends(get_current_user), db: Session = Depends(get_db)):
    
    access_token = current_user.token
    
    access_token_expiry = current_user.expires_at
    
    blacklist_token(access_token,access_token_expiry)


    now = datetime.now(timezone.utc)

    incoming_refresh_token= request.cookies.get("refresh_token")

    if incoming_refresh_token:
        db_refresh_token = db.query(database_models.Refresh_Tokens).filter(database_models.Refresh_Tokens.token == incoming_refresh_token).first()

        if db_refresh_token:

            db_refresh_token.revoked_at = now
            db_refresh_token.replaced_by_token = "Logout"
            db_refresh_token.last_used_at = now
    
    db.commit()

    response.delete_cookie(
    key="refresh_token",
        httponly=True,
    )

    return {"message":"Logout Successfully Done"}





# GET all products
@app.get("/products", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()


# GET product by id
@app.get("/products/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):

    db_product_by_id = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product_by_id:
        return db_product_by_id

    raise HTTPException(status_code=404, detail="Product not found")


# POST create product
@app.post("/products", status_code=201,response_model=ProductResponse)
def create_product(product: ProductCreate,current_user : AuthContext = Depends(require_role("admin")), db: Session = Depends(get_db)):
    
    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)

    db.commit()
    db.refresh(db_product)
    return db_product


# PUT replace product (full update)
@app.put("/products/{id}", response_model = ProductResponse)
def replace_product(id: int, product: ProductCreate,current_user: AuthContext = Depends(require_role("admin")), db: Session = Depends(get_db)):
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
@app.delete("/products/{id}", status_code=204)
def delete_product(id: int, current_user: AuthContext = Depends(require_role("admin")), db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return 
    
    raise HTTPException(status_code=404, detail="Product not found")

# PATCH update product (partial update)
@app.patch("/products/{id}", response_model=ProductResponse)
def update_product(id: int, product_update: ProductUpdate, current_user: AuthContext = Depends(require_role("admin")), db: Session = Depends(get_db)):
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