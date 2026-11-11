"""Seed generic developers.

Revision ID: a41c9d7e2b63
Revises: 287fddf9d125
Create Date: 2026-11-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "a41c9d7e2b63"
down_revision: Union[str, Sequence[str], None] = "287fddf9d125"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


developers = sa.table(
    "developer",
    sa.column("email", postgresql.CITEXT()),
    sa.column("first_name", sa.Text()),
    sa.column("last_name", sa.Text()),
)

SEED_DEVELOPERS = (
    {
        "email": "casey.nguyen@example.invalid",
        "first_name": "Casey",
        "last_name": "Nguyen",
    },
    {
        "email": "jordan.lee@example.invalid",
        "first_name": "Jordan",
        "last_name": "Lee",
    },
    {
        "email": "riley.patel@example.invalid",
        "first_name": "Riley",
        "last_name": "Patel",
    },
)


def upgrade() -> None:
    op.bulk_insert(developers, list(SEED_DEVELOPERS))


def downgrade() -> None:
    for developer in SEED_DEVELOPERS:
        op.execute(
            developers.delete().where(
                developers.c.email == developer["email"],
                developers.c.first_name == developer["first_name"],
                developers.c.last_name == developer["last_name"],
            )
        )
