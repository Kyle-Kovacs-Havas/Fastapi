"""add content column to posts table

Revision ID: 17680bf9c1a0
Revises: f37193071a62
Create Date: 2024-11-04 12:31:26.680734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17680bf9c1a0'
down_revision: Union[str, None] = 'f37193071a62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Post", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("Post", 'content')
    pass
