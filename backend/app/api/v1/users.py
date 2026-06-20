import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas.users import (
    UserCreate,
    UserLogin,
    TokenResponse,
    UserResponse,
    UserAdminUpdate
    )
from app.core.security import verify_password, create_access_token
from app.core.enums import UserRole
from app.api.deps import get_current_user, require_admin
from app.models.users import Users


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    existing = crud.users.get_by_email(db, user_data.email)
    
    if existing:
        if not existing.is_active:
            raise HTTPException(
                409,
                "This account is disabled. Please contact the administrator."
                )

        raise HTTPException(status_code=409, detail="Email already registered.")
    
    new_user = crud.users.create(db, user_data, role=UserRole.USER)
    
    logger.info("New user registered: id=%s", new_user.id)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT access token.
    """
    user = crud.users.get_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(
            403,
            "Your account has been disabled. Please contact the administrator."
            )
    token = create_access_token(user_id=user.id, role=user.role.value)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _admin: Users = Depends(require_admin),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    ):
    return crud.users.get_all(db, limit=limit, offset=offset)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserAdminUpdate,
    db: Session = Depends(get_db),
    admin: Users = Depends(require_admin),
):
    """Update a user's role and/or active status (admin only)."""
    if user_id == admin.id:
        raise HTTPException(400, "You cannot modify your own account.")
    target = crud.users.get_by_id(db, user_id)
    if target is None:
        raise HTTPException(404, "User not found")
    return crud.users.admin_update(db, target, role=payload.role, is_active=payload.is_active)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: Users = Depends(require_admin),
):
    if user_id == admin.id:
        raise HTTPException(400, "You cannot delete your own account.")
    target = crud.users.get_by_id(db, user_id)
    if target is None:
        raise HTTPException(404, "User not found.")
    crud.users.delete(db, target)
    return None
