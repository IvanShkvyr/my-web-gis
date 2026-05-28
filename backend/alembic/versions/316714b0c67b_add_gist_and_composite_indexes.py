"""Add GiST index on phone_telemetry.geom and composite index on (user_id, timestamp)

Revision ID: 316714b0c67b
Revises: 0027557e994b
Create Date: 2026-05-16

Why: GiST index was commented out in migration 1f19d1108737.
     GeoAlchemy2 created it automatically on the DB side, but it is
     not tracked by Alembic. This migration registers it properly
     and adds a composite index for the common query pattern:
     WHERE user_id = X ORDER BY timestamp DESC.
"""
from typing import Sequence, Union

from alembic import op


revision: str = '316714b0c67b'
down_revision: Union[str, Sequence[str], None] = '0027557e994b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # GeoAlchemy2 may have already created this index automatically.
    # IF NOT EXISTS makes this migration idempotent — safe to run
    # regardless of whether the index exists or not.
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_phone_telemetry_geom
        ON phone_telemetry
        USING gist (geom)
    """)

    op.create_index(
        index_name='idx_phone_telemetry_user_timestamp',
        table_name='phone_telemetry',
        columns=['user_id', 'timestamp']
    )


def downgrade() -> None:
    op.drop_index(
        index_name='idx_phone_telemetry_user_timestamp',
        table_name='phone_telemetry'
    )
    # Note: we intentionally do NOT drop idx_phone_telemetry_geom here.
    # It was created by GeoAlchemy2 automatically and is tied to the
    # geometry column. Dropping it would require recreating the column.
    # It will be dropped automatically with DROP TABLE in migration 1f19d1108737.