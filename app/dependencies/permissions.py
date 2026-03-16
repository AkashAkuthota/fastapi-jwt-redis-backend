from fastapi import Depends, HTTPException, status
from app.dependencies.decodingtokens import get_current_user, AuthContext

def require_role(*roles: str):

    def role_checkers(current_user = Depends(get_current_user)) -> AuthContext:
        if current_user.user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
        
        return current_user
    

    return role_checkers
