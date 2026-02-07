from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from main import get_db
from jose import JWTError, jwt
import auth
import database_models
from datetime import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    
    try:
        payload = jwt.decode(token, auth.secret_key, algorithms= auth.ALGORITHM)

        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    
    except JWTError:
        raise credentials_exception

    
    user = db.query(database_models.User).filter(database_models.User.email == email).first()

    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="inactive user")
    
    revoked_token = db.query(database_models.RevokedToken).filter(database_models.RevokedToken.token == token, database_models.RevokedToken.expires_at > datetime.utcnow() ).first()
    
    if revoked_token:
        raise credentials_exception
    
    return user
    
    




