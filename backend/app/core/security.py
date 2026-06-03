from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
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

def create_access_token(user_id: int, role: Optional[str] = None) -> str:
    """
    Creates a signed JWT token containing user_id.
    """
    payload = {
      "sub": str(user_id),
      "exp": datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    if role is not None:
        payload["role"] = role
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> int | None:
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
