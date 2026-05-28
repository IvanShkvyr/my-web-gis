from pydantic import BaseModel, Field, EmailStr, ConfigDict

from app.core.constants import USERNAME_LENGTH, PASS_MIN_LEN, PASS_MAX_LEN
from app.core.enums import UserRole


class UserCreate(BaseModel):
    username: str = Field(max_length=USERNAME_LENGTH)
    email: EmailStr
    password: str = Field(min_length=PASS_MIN_LEN, max_length=PASS_MAX_LEN)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserAdminUpdate(BaseModel):
    role: UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

