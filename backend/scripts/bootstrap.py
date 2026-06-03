"""
Idempotent bootstrap: first ADMIN + a DEMO account with sample telemetry.
Admin credentials come from ENV VARS

PowerShell (from backend/):
    $env:BOOTSTRAP_ADMIN_EMAIL="admin@example.com"
    $env:BOOTSTRAP_ADMIN_PASSWORD="strong-pass-please-change"
    python -m scripts.bootstrap
"""
import os

from app.database import SessionLocal
from app.crud import users as users_crud
from app.crud import telemetry as telemetry_crud
from app.schemas.users import UserCreate
from app.schemas.telemetry import TelemetryCreate
from app.core.enums import UserRole


def ensure_admin(db) -> None:
    email = os.environ["BOOTSTRAP_ADMIN_EMAIL"]
    password = os.environ["BOOTSTRAP_ADMIN_PASSWORD"]
    if users_crud.get_by_email(db, email):
        print(f"[admin] already exists: {email}")
        return
    users_crud.create(
        db,
        UserCreate(username="admin", email=email, password=password),
        role=UserRole.ADMIN,
    )
    print(f"[admin] created: {email}")


def ensure_demo(db) -> None:
    demo = users_crud.get_by_email(db, "demo@example.com")
    if demo is None:
        demo = users_crud.create(
            db,
            UserCreate(username="demo", email="demo@example.com",
                       password="demo-password-123"),
            role=UserRole.DEMO,
        )
        print(f"[demo] user created: id={demo.id}")

    # сіємо точки тільки якщо їх ще нема (ідемпотентність)
    existing, _ = telemetry_crud.get_list_by_user(db, user_ids=[demo.id], limit=1)
    if existing:
        print("[demo] telemetry already present, skipping")
        return

    for lat, lon in [(50.4501, 30.5234), (50.4470, 30.5180), (50.4530, 30.5290)]:
        telemetry_crud.create(
            db,
            TelemetryCreate(latitude=lat, longitude=lon,
                            accel_x=0.0, accel_y=0.0, accel_z=0.0),
            user_id=demo.id,
        )
    print("[demo] telemetry seeded")


def main() -> None:
    db = SessionLocal()
    try:
        ensure_admin(db)
        ensure_demo(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()