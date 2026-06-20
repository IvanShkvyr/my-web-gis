from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy import Enum as SAEnum

from app.core.constants import USERNAME_LENGTH
from app.core.enums import UserRole
from app.models.base_class import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(USERNAME_LENGTH))
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(
        SAEnum(
            UserRole,
            name="user_role",
            values_callable=lambda x: [e.value for e in x],
            ),
        nullable=False,
        default=UserRole.USER,
        server_default=UserRole.USER.value
    )
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime, server_default=func.now())
