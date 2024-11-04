"""add user table

Revision ID: 2331efb2d972
Revises: 17680bf9c1a0
Create Date: 2024-11-04 12:34:47.999829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2331efb2d972'
down_revision: Union[str, None] = '17680bf9c1a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
        sa.Column('id',sa.Integer, primary_key = True, nullable=False),
        sa.Column('email',sa.String, nullable=False, unique=True),
        sa.Column('password',sa.String, nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True), 
                        nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
