from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app import crud
from app.core.enums import UserRole
from app.database import get_db
from app.models.users import Users
from app.core.security import decode_token


_optional_bearer = HTTPBearer(auto_error=False)


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_optional_bearer),
    db: Session = Depends(get_db),
    ) -> Optional[Users]:
    """
    Return the current User object if a valid token is provided.
    Returns None for anonymous requests OR invalid/expired tokens.
    """
    if credentials is None:
        return None

    user_id = decode_token(credentials.credentials)
    if not user_id:
        return None

    return crud.users.get_by_id(db, user_id)


def get_current_user(
    user: Optional[Users] = Depends(get_optional_current_user),
    ) -> Users:
    """Require an authenticated, existing user. 401 otherwise."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


def require_admin(
    user: Users = Depends(get_current_user),
    ) -> Users:
    """Require ADMIN role. 403 otherwise."""
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user
