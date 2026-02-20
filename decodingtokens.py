from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import auth
import database_models
from database import get_db
from auth_context import AuthContext
from datetime import datetime, timezone
from redis_client import is_token_blacklisted



for_token_extraction = HTTPBearer()

def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(for_token_extraction), db: Session = Depends(get_db)) -> AuthContext:

    token = credentials.credentials

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms= [auth.ALGORITHM])

        user_id = payload.get("user_id")
        exp_timestamp = payload.get("exp")

        if user_id is None or exp_timestamp is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    if  is_token_blacklisted(token):
        raise credentials_exception
    
    user = db.query(database_models.User).filter(database_models.User.user_id == user_id).first()

    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="inactive user")
    
    
    return AuthContext(
        user=user,
        token=token,
        expires_at=datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    )
    




