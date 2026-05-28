from typing import Optional

from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.users import Users
from app.core.security import _decode_token


_optional_bearer = HTTPBearer(auto_error=False)


def get_optional_current_uaer(
    request: Request,
    db: Session = Depends(get_db),
    ) -> Optional[Users]:
    """
    Return the current User object if a valid token is provided.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1]
    user_id = _decode_token(token)
    if not user_id:
        return None

    return db.query(Users).filter(Users.id == user_id).first()
