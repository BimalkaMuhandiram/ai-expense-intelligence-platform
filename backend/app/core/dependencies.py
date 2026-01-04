from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def require_admin(user_id: str = Depends(get_current_user)):
    # for now, assume admin manually
    if user_id != "admin":
        raise HTTPException(status_code=403, detail="Admin only")