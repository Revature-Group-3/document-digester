"""enable citext extension

Revision ID: 653edca717b0
Revises: 
Create Date: 2026-11-11 13:34:28.063346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '653edca717b0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")


def downgrade() -> None:
    """Downgrade schema."""
    pass
