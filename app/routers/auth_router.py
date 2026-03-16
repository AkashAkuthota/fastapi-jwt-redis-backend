from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.schemas.model import UserCreate, UserResponse, UserLogin
from app.db.database import get_db
import app.db.database_models as database_models

import app.core.security as security
import app.core.auth as auth

from app.dependencies.decodingtokens import get_current_user
from app.dependencies.auth_context import AuthContext

from app.core.redis_client import redis_client, blacklist_token
from app.core.rate_limiter import check_login_rate_limits, check_refresh_rate_limit


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# SIGNUP
@router.post("/signup", status_code=201, response_model=UserResponse)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):

    email = user.email.lower()

    existing_user = db.query(database_models.User).filter(
        database_models.User.email == email
    ).first()

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already Exists")

    hashed_password = security.get_password_hash(user.password)

    db_user = database_models.User(
        email=email,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# LOGIN
@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLogin, request: Request, response: Response, db: Session = Depends(get_db)):

    email = user.email.lower()

    client_ip = request.client.host
    check_login_rate_limits(client_ip, email)

    db_user = db.query(database_models.User).filter(
        database_models.User.email == email
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="inactive user")

    redis_client.delete(f"login:ip:{client_ip}")
    redis_client.delete(f"login:email:{email}")

    access_token = auth.create_access_token(
        data={"sub": db_user.email, "user_id": db_user.user_id, "role": db_user.role}
    )

    refresh_token = auth.create_refresh_token()

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)

    db_refresh_token = database_models.Refresh_Tokens(
        token=refresh_token,
        user_id=db_user.user_id,
        expires_at=expires_at,
        revoked_at=None,
        created_at=now,
        replaced_by_token=None,
        last_used_at=None,
    )

    db.add(db_refresh_token)
    db.commit()
    db.refresh(db_refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=auth.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# REFRESH TOKEN
@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):

    incoming_token = request.cookies.get("refresh_token")

    if incoming_token is None:
        raise HTTPException(status_code=401, detail="Refresh Token Missing")

    db_refresh_token = db.query(database_models.Refresh_Tokens).filter(
        database_models.Refresh_Tokens.token == incoming_token
    ).first()

    if not db_refresh_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    now = datetime.now(timezone.utc)

    if db_refresh_token.expires_at <= now:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user = db.query(database_models.User).filter(
        database_models.User.user_id == db_refresh_token.user_id
    ).first()

    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User invalid")

    client_ip = request.client.host
    user_id = db_refresh_token.user_id

    check_refresh_rate_limit(client_ip, user_id)

    new_refresh_token = auth.create_refresh_token()
    new_expiry = now + timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)

    db_refresh_token.revoked_at = now
    db_refresh_token.replaced_by_token = new_refresh_token
    db_refresh_token.last_used_at = now

    new_db_refresh = database_models.Refresh_Tokens(
        token=new_refresh_token,
        user_id=user.user_id,
        expires_at=new_expiry,
        created_at=now,
        replaced_by_token=None,
        revoked_at=None,
        last_used_at=None,
    )

    db.add(new_db_refresh)
    db.commit()

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=auth.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    access_token = auth.create_access_token(
        data={"sub": user.email, "user_id": user.user_id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# LOGOUT
@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    request: Request,
    response: Response,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    access_token = current_user.token
    access_token_expiry = current_user.expires_at

    blacklist_token(access_token, access_token_expiry)

    now = datetime.now(timezone.utc)

    incoming_refresh_token = request.cookies.get("refresh_token")

    if incoming_refresh_token:

        db_refresh_token = db.query(database_models.Refresh_Tokens).filter(
            database_models.Refresh_Tokens.token == incoming_refresh_token
        ).first()

        if db_refresh_token:
            db_refresh_token.revoked_at = now
            db_refresh_token.replaced_by_token = "Logout"
            db_refresh_token.last_used_at = now

    db.commit()

    response.delete_cookie(
        key="refresh_token",
        httponly=True
    )

    return {"message": "Logout Successfully Done"}