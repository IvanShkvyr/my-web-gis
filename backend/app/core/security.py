from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.core.constants import JWT_ALGORITHM


# ----------------------- Password hashing -----------------------

def hash_password(plain_password: str) -> str:
    """
    Return bcrypt hash of a plain-text password.
    """
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Return True if plain_password mathches the stored hash.
    """
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# ------------------------- JWT ---------------------------------

def create_access_token(user_id: int) -> str:
    """
    Creates a signed JWT token containing user_id.
    """
    payload = {
      "sub": str(user_id),
      "exp": datetime.now(timezone.utc) +
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)


def _decode_token(token: str) -> int | None:
    """
    Decodes JWT and return user_id, or None if invalid/expired.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM]
            )
        user_id = payload.get("sub")
        return int(user_id) if user_id else None
    except JWTError:
        return None
    

# ---------------------- FastAPI dependency ----------------------

bearer_scheme = HTTPBearer()


def get_current_user_id(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
        ) -> int:
    """
    FastAPI dependency
    Validates Bearer token and returns user_id.
    Raises 401 if token is missing, invalid, or expired.
    """
    user_id = _decode_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return user_id




