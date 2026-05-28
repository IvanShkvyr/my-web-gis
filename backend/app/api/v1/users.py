import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas.users import UserCreate, UserLogin, TokenResponse, UserResponse
from app.core.security import verify_password, create_access_token
from app.core.enums import UserRole


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    existing = crud.users.get_by_email(db, user_data.email)
    
    if existing:
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
    
    token = create_access_token(user_id=user.id)

    return {"access_token": token, "token_type": "bearer"}
