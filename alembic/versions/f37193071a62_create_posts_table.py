"""create posts table

Revision ID: f37193071a62
Revises: 
Create Date: 2024-11-04 12:24:40.448878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f37193071a62'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("Post", sa.Column("id", sa.Integer(), nullable=False, primary_key=True)
                    , sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("Post")
    pass
