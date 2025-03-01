"""add content column to posts table

Revision ID: a2f9c60bb8bb
Revises: 0b9b868d4d4e
Create Date: 2025-02-27 21:07:06.882197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2f9c60bb8bb'
down_revision: Union[str, None] = '0b9b868d4d4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
