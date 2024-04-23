"""create users table

Revision ID: 6541bb6516b1
Revises: 
Create Date: 2024-04-23 10:51:03.134023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '6541bb6516b1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True,
                              index=True, nullable=False),
                    sa.Column("username", sa.String,
                              index=True, nullable=False),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("first_name", sa.String, nullable=False),
                    sa.Column("last_name", sa.String, nullable=False),
                    sa.Column("is_active", sa.Boolean,
                              server_default="true", nullable=False),
                    sa.Column("created_at", sa.DateTime(timezone=True),
                              nullable=False),
                    sa.Column("updated_at", sa.DateTime(timezone=True),
                              nullable=False),
                    sa.UniqueConstraint("username", name="users_username_unique_constraint"))


def downgrade() -> None:
    op.drop_table("users")
