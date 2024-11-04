"""add last columns to posts table

Revision ID: 4d66171c5c72
Revises: 854e2bdde9fc
Create Date: 2024-11-04 12:43:56.136249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d66171c5c72'
down_revision: Union[str, None] = '854e2bdde9fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Post", sa.Column("published", sa.Boolean(), 
        nullable=False, server_default="TRUE"))
    op.add_column("Post", sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
        nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column("Post","published")
    op.drop_column("Post","created_at")
    pass
