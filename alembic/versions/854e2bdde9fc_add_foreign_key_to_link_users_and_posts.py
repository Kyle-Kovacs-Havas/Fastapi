"""add foreign key to link users and posts

Revision ID: 854e2bdde9fc
Revises: 2331efb2d972
Create Date: 2024-11-04 12:40:16.293208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '854e2bdde9fc'
down_revision: Union[str, None] = '2331efb2d972'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Post", sa.Column("owner_id", sa.Integer(),nullable=False))
    op.create_foreign_key("Post_users_fk", source_table="Post", 
                          referent_table="users", local_cols=["owner_id"], 
                          remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("Post_users_fk", table_name="Post")
    op.drop_column("Post", "owner_id")
    pass
