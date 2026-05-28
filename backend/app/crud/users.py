from sqlalchemy.orm import Session

from app.models.users import Users
from app.schemas.users import UserCreate
from app.core.security import hash_password
from app.core.enums import UserRole


def get_demo_user_ids(db: Session) -> list[int]:
    """
    Return list of IDs of all users with DEMO role.
    """
    rows = db.query(Users.id).filter(Users.role == UserRole.DEMO).all()

    return [row.id for row in rows]



def get_by_email(db: Session, email: str) -> Users | None:
    """
    Return user by email, or None if not found
    """
    return db.query(Users).filter(Users.email == email).first()


def get_by_id(db: Session, user_id: int) -> Users | None:
    """
    Return user by primary key, or None if not found
    """
    return db.query(Users).filter(Users.id == user_id).first()


def create(
        db: Session,
        user_data: UserCreate,
        role: UserRole = UserRole.USER
        ) -> Users:
    """
    Create a new user and persists it to the database
    """
    new_user = Users(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password),
        role=role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
