import logging
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app import crud
from app.core.enums import UserRole
from app.database import get_db
from app.models.users import Users
from app.schemas.telemetry import (
    TelemetryCreate,
    TelemetryResponse,
    TelemetryPage
    )
from app.core.config import settings
from app.api.deps import (
    get_optional_current_user,
    get_current_user,
    require_admin
    )


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/telemetry", tags=["telemetry"])


@router.post("", response_model=TelemetryResponse, status_code=201)
def create_telemetry(
    data: TelemetryCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
    ):
    """
     Receives sensor data from a mobile device and stores it in the database.
    """
    if current_user != UserRole.ADMIN:
        if crud.telemetry.count_by_user(db, current_user.id) >= settings.MAX_TELEMETRY_PER_USER:
            raise HTTPException(
                429,
                "Telemetry quota reached. Delete old records to continue."
                )
    try:
        record = crud.telemetry.create(db, data, user_id=current_user.id)
        return record

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Data conflict. Possibly duplicate or invalid reference.",
            )
    
    except SQLAlchemyError:
        logger.exception("Failed to create telemetry")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
            )


def _resolve_target_user_ids(
        current_user: Optional[Users],
        requested_ids: Optional[list[int]],
        db: Session,
) -> list[int]:
    """
    Determine which user_ids to query based on role and request params.

    Anonymous / no token  → demo users
    USER / DEMO           → own id only (requested_ids ignored)
    ADMIN, no filter      → demo users
    ADMIN + ?user_id=...  → requested ids
    """
    if current_user is None:
        return crud.users.get_demo_user_ids(db)
    
    if current_user.role in (UserRole.USER,  UserRole.DEMO):
        return [current_user.id]
    
    if current_user.role == UserRole.ADMIN:
        if requested_ids:
            return requested_ids
        return crud.users.get_demo_user_ids(db)

    return [current_user.id]


@router.get("", response_model=TelemetryPage)
def get_telemetry(
    db: Session = Depends(get_db),
    current_user: Optional[Users] = Depends(get_optional_current_user),
    user_id: Optional[list[int]] = Query(None, description="Filter by user ID (admin only, repeatable)"),
    date_from: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    ):
    """
    Return current user's telemetry records
    """
    try:
        target_ids = _resolve_target_user_ids(current_user, user_id, db)

        if not target_ids:
            return TelemetryPage(total=0, limit=limit, offset=offset, items=[])


        records, total = crud.telemetry.get_list_by_user(
            db,
            user_ids=target_ids,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
            )

        return TelemetryPage(
            total=total,
            limit=limit,
            offset=offset,
            items=records,
            )

    except SQLAlchemyError:
        logger.exception(
                        "Failed to fetch telemetry for user-id=%s",
                        current_user.id if current_user else "anonymous",
                        )
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.delete("/by-user/{user_id}", status_code=204)
def delete_user_telemetry(
    user_id: int,
    db: Session = Depends(get_db),
    _admin: Users = Depends(require_admin),
    ):
    """
    Delete all telemetry of a given user. Admin only. Keeps the user account.
    """
    crud.telemetry.delete_by_user(db, user_id)
    return None


